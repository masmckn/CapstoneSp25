const express = require('express');
const app = express();
app.set('view engine', 'pug');
app.use(express.static('public'));
const cors = require('cors');

app.use(cors())

app.get('/', (req, res) => {
    res.sendFile(__dirname + '/public/login.html'); // Serve index.html from a 'public' directory
});  

// Server activation
const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
  console.info(`Server running on port ${PORT}`);
});