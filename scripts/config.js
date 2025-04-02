import * as dotenv from 'dotenv';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const pathString = path.join(__dirname, '..', '.env.development')
dotenv.config({ path: path.join(__dirname, '..', '.env.development'), debug: true });


const server = process.env.AZURE_SQL_SERVER;
const database = process.env.AZURE_SQL_DATABASE;
const port = +process.env.AZURE_SQL_PORT;
const type = process.env.AZURE_SQL_AUTHENTICATIONTYPE;

console.log("Config values:", {
  server, 
  database, 
  port, 
  type,
});

const config = {
  server,
  port,
  database,
  authentication: {
    type
  },
  options: {
      encrypt: true,
      clientId: process.env.AZURE_CLIENT_ID  // <----- user-assigned managed identity        
  }
};

export default config;