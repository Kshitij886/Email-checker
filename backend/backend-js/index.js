// const express = require("express");
const axios = require("axios");
const { ImapFlow } = require("imapflow");
// const cors = require("cors");
const { simpleParser } = require("mailparser");


(async () => {
  const client = new ImapFlow({
    host: "imap.migadu.com",
    secure: true,
    prot: 993,
    auth: {
      user: "sakshyam@tivazo.com",
      pass: "",
    },
    logger: false,
  });

  await client.connect();
  console.log("Connection sucessful");
  const lock = await client.getMailboxLock("INBOX");
  try {
    console.log("Waiting for email to receive....");
    client.on("exists", async () => {
      console.log("EMAIL received");
      const message = await client.fetchOne(client.mailbox.exists, {
        source: true,
      });
      const parsed_message = await simpleParser(message.source);
      const links = [];
      const url_regrex =
        /<?(?:(?:https?|ftp|file):\/\/|www\.|ftp\.)(?:\([-A-Z0-9+&@#/%=~_|$?!:,.]*\)|[-A-Z0-9+&@#/%=~_|$?!:,.])*(?:\([-A-Z0-9+&@#/%=~_|$?!:,.]*\)|[A-Z0-9+&@#/%=~_|$])>?/gi;
      if (parsed_message.text) {
        links.push(parsed_message.text.match(url_regrex));
      } else if (parsed_message.html) {
        links.push(parsed_message.html.match(url_regrex));
      }
      console.log(links)
      let attachment = null
      if (parsed_message.attachments && parsed_message.attachments.length > 0) {
        const firstAttachment = parsed_message.attachments[0];
        attachment = {
          content: firstAttachment.content, // Buffer
          filename: firstAttachment.filename,
        };
      }
      console.log(attachment)
       const result = await axios.post("http://127.0.0.1:5000/api/check_email", {
         body: parsed_message.text,
         attachment: attachment, 
         url: links,
       });
       console.log(result.data);
    });
  } catch (err) {
    console.log("Error: ", err.message);
  } finally {
    lock.release();
  }
})();


