import sql from 'mssql';

let database = null;

export default class Database {
  config = {};
  poolconnection = null;
  connected = false;

  constructor(config) {
    this.config = config;
  }

  async connect() {
    try {
      console.log(`Database connecting...${this.connected}`);
      if (this.connected === false) {
        this.poolconnection = await sql.connect(this.config);
        this.connected = true;
        console.log('Database connection successful');
      } else {
        console.log('Database already connected');
      }
    } catch (error) {
      console.error(`Error connecting to database: ${JSON.stringify(error, Object.getOwnPropertyNames(error))}`);
    }
  }

  async disconnect() {
    try {
      if (this.connected) {
        await this.poolconnection.close();
        this.connected = false;
        console.log('Database disconnected successfully.');
      } else {
        console.log('Database already disconnected')
      }
    } catch (error) {
      console.error('Error disconnecting from the database:', error);
    }
  }

  async executeQuery(query) {
    const request = this.poolconnection.request();
    const result = await request.query(query);

    return result.rowsAffected[0];
  }

  async create(data) {
    const request = this.poolconnection.request();

    request.input('userid', sql.NVarChar(255), data.userid);
    request.input('password', sql.NVarChar(255), data.password);

    const result = await request.query(
      `INSERT INTO [User] (userid, pass) VALUES (@firstName, @lastName)`
    );

    return result.rowsAffected[0];
  }

  async readAll() {
    const request = this.poolconnection.request();
    const result = await request.query(`SELECT * FROM Person`);

    return result.recordsets[0];
  }

  async read(id) {
    const request = this.poolconnection.request();
    const result = await request
      .input('id', sql.Int, +id)
      .query(`SELECT * FROM Person WHERE id = @id`);

    return result.recordset[0];
  }

  async update(id, data) {
    const request = this.poolconnection.request();

    request.input('id', sql.Int, +id);
    request.input('firstName', sql.NVarChar(255), data.firstName);
    request.input('lastName', sql.NVarChar(255), data.lastName);

    const result = await request.query(
      `UPDATE Person SET firstName=@firstName, lastName=@lastName WHERE id = @id`
    );

    return result.rowsAffected[0];
  }

  async delete(id) {
    const idAsNumber = Number(id);

    const request = this.poolconnection.request();
    const result = await request
      .input('id', sql.Int, idAsNumber)
      .query(`DELETE FROM Person WHERE id = @id`);

    return result.rowsAffected[0];
  }
}

export const createDatabaseConnection = async (config) => {
  database = new Database(config);
  await database.connect();
  return database;
};