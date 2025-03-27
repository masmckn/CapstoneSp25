const express = require('express');
const app = express();
app.set('view engine', 'pug');
app.use(express.static('public'));
const cors = require('cors');

app.use(cors())

app.get('/', (req, res) => {
      res.sendFile('index.html')
})

// Server activation
const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
  console.info(`Server running on port ${PORT}`);
});