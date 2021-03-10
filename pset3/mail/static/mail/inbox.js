document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  
  // compose email
  document.querySelector('#compose-form').onsubmit = send_email;

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email(event, recipient = null, subject = null, body = null, timestamp = null) {
  if (subject !== null && subject.substr(0, 2) !== 'Re:') {
    subject = `Re: ${subject}`;
  }

  if (body !== null) {
    body = `On ${timestamp} ${recipient} wrote: ${body}`;
  }

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = recipient ?? '';
  document.querySelector('#compose-subject').value = subject;
  document.querySelector('#compose-body').value = body;
}

function load_mailbox(mailbox) {
  view = document.querySelector('#emails-view');

  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(result => {
    if (result.length > 0) {
      result.forEach(mail => {
        const element = document.createElement('div')
        let content = `
          ${mailbox === 'inbox' ? mail.sender : mail.recipients.join(', ')} <strong>${mail.subject}</strong>
          ${mailbox === 'inbox' ? `<button onClick="archive(event, ${mail.id})" style="float:right;margin-left:10px;">Archive</button>` : ''}
          <span style="float:right">${mail.timestamp}</span>
        `;

        element.innerHTML = content;
        element.style.border = '1px solid #ccc';
        element.style.padding = '10px';
        element.style.cursor = 'pointer';
        element.style.background = mail.read ? '#eee' : 'white'
        element.onclick = load_email.bind(null, mail.id);
        view.append(element);
      })
    }
  })
  .catch(error => {
    console.log('error', error);
  })
  
  // Show the mailbox and hide other views
  view.style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  view.innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
}

function send_email(event) {
  event.preventDefault();

  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: document.querySelector('#compose-recipients').value,
        subject: document.querySelector('#compose-subject').value,
        body: document.querySelector('#compose-body').value
    })
  })
  .then(response => response.json())
  .then(result => {
    if (result.error) {
      alert(result.error)
    } else {
      load_mailbox('sent')
    }
  })
  .catch(error => {
    console.log('error', error);
  });
}

function load_email(id) {
  view = document.querySelector('#emails-view');
  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(mail => {
    if (!mail.read) {
      mark_email_as_read(id);
    }

    view.innerHTML = `
      <p><strong>From: </strong> ${mail.sender}</p>
      <p><strong>To: </strong> ${mail.recipients.join(', ')}</p>
      <p><strong>Subject: </strong> ${mail.subject}</p>
      <p><strong>Timestamp: </strong> ${mail.timestamp}</p>
      <p>
        <button onClick="compose_email(event, '${mail.sender}', '${mail.subject}', '${mail.body}', '${mail.timestamp}')">Reply</button> 
        ${mail.archived ? `<button onClick="unarchive(event, ${mail.id})">Unarchive</button>` : ''}
      </p>
      <hr>
      ${mail.body}
    `;
  })
  .catch(error => {
    console.log('error', error);
  })
  
  // Show the mailbox and hide other views
  view.style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
}

function mark_email_as_read(id) {
  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
        read: true
    })
  })
}

function unarchive(event, id) {
  event.stopPropagation();
  event.preventDefault();

  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: false
    })
  })
  .then(result => load_mailbox('inbox'))
  .catch(error => console.log(error))
}

function archive(event, id) {
  event.stopPropagation();
  event.preventDefault();

  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: true
    })
  })
  .then(result => load_mailbox('inbox'))
  .catch(error => console.log(error))
}