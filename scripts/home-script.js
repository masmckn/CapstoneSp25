import express from 'express';
import path from 'path';
import bodyParser from 'body-parser';
import cors from 'cors';
import user from './user.js';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true })); 
app.set('view engine', 'pug');
app.use(express.static('public'));
app.use(cors());

app.get('/(login)?', (req, res) => {
    res.sendFile('login.html', { root: path.join(__dirname, '../public') }); // Serve login.html from the 'public' directory
});

app.get('/createaccount', (req, res) => {
    res.sendFile('createaccount.html', { root: path.join(__dirname, '../public') });
});

app.post('/dashboard', (req, res, next) => {
    console.log(req.body);
    next();
}, user);

// Server activation
const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
  console.info(`Server running on port ${PORT}`);
});