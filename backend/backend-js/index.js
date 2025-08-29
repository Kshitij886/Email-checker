const Imap = require('node-imap');

const imap = new Imap({
    user: '',
    password: '',
    host: 'imap.migadu.com',
    port: 993,
    tls: true
});

function openInbox (cb){
    imap.openBox('INBOX', true, cb)
}

imap.once('ready', function() {
  openInbox(function(err, box) {
    if (err) throw err;
    var f = imap.seq.fetch('1:3', {
      bodies: 'HEADER.FIELDS (FROM TO SUBJECT DATE)',
      struct: true
    });
    f.on('message', function(msg, seqno) {
      console.log('Message #%d', seqno);
      var prefix = '(#' + seqno + ') ';
      console.log(prefix)
      msg.on('body', function(stream, info) {
        var buffer = '';
        stream.on('data', function(chunk) {
          buffer += chunk.toString('utf8');
        });
        stream.once('end', function() {
          console.log('Parsed header: %s', Imap.parseHeader(buffer));
        });
      });
      msg.once('attributes', function(attrs) {
        console.log('Attributes: %s', attrs, false, 8);
      });
      msg.once('end', function() {
        console.log(prefix + 'Finished');
      });
    });
    f.once('error', function(err) {
      console.log('Fetch error: ' + err);
    });
    f.once('end', function() {
      console.log('Done fetching all messages!');
      imap.end();
    });
  });
});

imap.once('error', (err) => {
    console.error('IMAP error:', err);
});

imap.once('end', function(){
    console.log('connection ended.')
})

imap.connect();