import express from 'express';
import config from './config.js';
import { createDatabaseConnection } from './database.js';
import path from 'path';
import { fileURLToPath } from 'url';
import * as EmailValidator from 'email-validator';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const router = express.Router();
router.use(express.json());

console.log("Config values (user):", {
    server: config.server, 
    config: config.database, 
    port: config.port, 
    type: config.authentication.type,
  });

const database = await createDatabaseConnection(config);

router.get('/', async (req, res) => {
  /* try {
    // Return a list of persons

    const persons = await database.readAll();
    console.log(`persons: ${JSON.stringify(persons)}`);
    res.status(200).json(persons);
  } catch (err) {
    res.status(500).json({ error: err?.message });
  }*/
});

router.post('/dashboard(.html)?', async (req, res) => {
  try {
    const params = Object.keys(req.body);
    console.log('About to evaluate if statement.');
    if(params.includes('first_name')){
      console.log('New user.');
      const newUser = req.body;
      console.log(`newUser: ${JSON.stringify(newUser)}`);
      if(newUser.password === newUser.confirm_password){
        const result = await database.executeQuery(
          `INSERT INTO [User] (UserID, FirstName, LastName, Email, PassHash) VALUES
          (\'${newUser.username}\', \'${newUser.first_name}\', \'${newUser.last_name}\', 
          \'${newUser.email}\', \'${newUser.password}\')`);
        console.log('Query executed.');
        res.sendFile('login.html', { root: path.join(__dirname, '../public') });
      }
      else{
        res.send('Passwords did not match. Please try again.');
      }
    }
    else {
      const user = req.body;
      console.log(`user: ${JSON.stringify(user)}`);
      const result = await database.executeQuery(`SELECT * FROM [User] WHERE UserID = \'${user.userid}\'`);
      console.log(`result: ${JSON.stringify(result)}`)
      if(result){
        console.log('UserID found in database.');
        //check password goes here
        const passResult = 1;
        if(passResult){
          res.sendFile('dashboard.html', { root: path.join(__dirname, '../') });
        }
        else{
          res.send('Wrong UserID or password. Please try again.');
        }
      }
      else{
        res.send('Wrong UserID or password. Please try again.');
      }
    }
  } catch (err) {
    res.status(500).json({ error: err?.message });
  }
});

router.get('/:id', async (req, res) => {
  try {
    // Get the person with the specified ID
    const personId = req.params.id;
    console.log(`personId: ${personId}`);
    if (personId) {
      const result = await database.read(personId);
      console.log(`persons: ${JSON.stringify(result)}`);
      res.status(200).json(result);
    } else {
      res.status(404);
    }
  } catch (err) {
    res.status(500).json({ error: err?.message });
  }
});

router.put('/:id', async (req, res) => {
  try {
    // Update the person with the specified ID
    const personId = req.params.id;
    console.log(`personId: ${personId}`);
    const person = req.body;

    if (personId && person) {
      delete person.id;
      console.log(`person: ${JSON.stringify(person)}`);
      const rowsAffected = await database.update(personId, person);
      res.status(200).json({ rowsAffected });
    } else {
      res.status(404);
    }
  } catch (err) {
    res.status(500).json({ error: err?.message });
  }
});

router.delete('/:id', async (req, res) => {
  try {
    // Delete the person with the specified ID
    const personId = req.params.id;
    console.log(`personId: ${personId}`);

    if (!personId) {
      res.status(404);
    } else {
      const rowsAffected = await database.delete(personId);
      res.status(204).json({ rowsAffected });
    }
  } catch (err) {
    res.status(500).json({ error: err?.message });
  }
});

export default router;