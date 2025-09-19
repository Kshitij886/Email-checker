const express = require("express");
const axios = require("axios");
const { ImapFlow } = require("imapflow");
const cors = require("cors");
const { simpleParser } = require("mailparser");

const app = express();
const PORT = 5000;

app.use(cors());
app.use(express.json());

let client = null;
let lock = null;
let listening = false;

app.post("/api-firewall", async (req, res) => {
  const { status } = req.body;

  if (status === true) {
    if (listening) {
      return res.send({ message: "Firewall already active and listening for new emails." });
    }

    client = new ImapFlow({
      host: "imap.migadu.com",
      secure: true,
      port: 993,
      auth: {
        user: "kshitiz@tivazo.com",
        pass: "Kshitiz@123",
      },
      logger: false,
    });

    await client.connect();
    console.log("Connection successful");

    lock = await client.getMailboxLock("INBOX");
    listening = true;

    console.log("Firewall activated. Waiting for new emails...");

    client.on("exists", async () => {
      console.log("EMAIL received");

      try {
        const message = await client.fetchOne(client.mailbox.exists, { source: true });
        const parsed_message = await simpleParser(message.source);

        const url_regex =
          /<?(?:(?:https?|ftp|file):\/\/|www\.|ftp\.)(?:\([-A-Z0-9+&@#/%=~_|$?!:,.]*\)|[-A-Z0-9+&@#/%=~_|$?!:,.])*(?:\([-A-Z0-9+&@#/%=~_|$?!:,.]*\)|[A-Z0-9+&@#/%=~_|$])>?/gi;

        let links = [];
        if (parsed_message.text) links = parsed_message.text.match(url_regex) || [];
        else if (parsed_message.html) links = parsed_message.html.match(url_regex) || [];

        let attachment = null;
        if (parsed_message.attachments && parsed_message.attachments.length > 0) {
          const firstAttachment = parsed_message.attachments[0];
          attachment = {
            content: firstAttachment.content,
            filename: firstAttachment.filename,
          };
        }
        console.log(attachment,links)
        const result = await axios.post("http://127.0.0.1:5000/api/check_email", {
          body: parsed_message.text,
          attachment,
          url: links,
        });

        console.log(result.data);

        if (result.data.status === true && message.uid) {
          await client.messageMove(message.uid, "Trash");
          console.log("Corrupt email detected and moved to trash.");
        }
        console.log("Waiting for new email...");
      } catch (error) {
        console.log("Error processing email:", error.message);
      }
    });

    return res.send({ message: "Firewall activated and listening for emails." });

  } else if (status === false) {
    if (client && listening) {
      try {
        await lock.release();
        await client.logout();
        listening = false;
        console.log("Firewall deactivated. Stopped listening for emails.");
        return res.send({ message: "Firewall deactivated." });
      } catch (err) {
        console.log("Error stopping firewall:", err.message);
        return res.status(500).send({ error: err.message });
      }
    } else {
      return res.send({ message: "Firewall is already inactive." });
    }
  } else {
    return res.status(400).send({ error: "Invalid status value. Must be true or false." });
  }
});

app.listen(PORT, () => {
  console.log(`Server is listening on port ${PORT}`);
});
