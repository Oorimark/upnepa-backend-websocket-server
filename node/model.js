import fs from "fs";

export default class FileStorage {
  /* OTP SERVICE STORAGE WORKER: store pending otp */

  static fileName = "temp.db";
  static MAX_FILE_LENGTH = 5;

  constructor() {
    if (!this.readFile()) {
      this.writeFile([]);
    }
  }

  readFile() {
    try {
      const data = fs.readFileSync(FileStorage.fileName, "utf8");
      return JSON.parse(data) || data;
    } catch (error) {
      return null;
    }
  }

  writeFile(updatedContent) {
    fs.writeFileSync(
      FileStorage.fileName,
      JSON.stringify(updatedContent, null, 5)
    );
  }

  saveData(data) {
    let db = this.readFile();
    if (db.length >= FileStorage.MAX_FILE_LENGTH) db = db.slice(2);
    db.push(data);
    this.writeFile(db); // update db
  }

  deleteData(otp) {
    const db = this.readFile();
    const updatedContent = db.filter((data) => data.otp !== otp);
    this.writeFile(updatedContent);
  }

  findOtp(otp) {
    const db = this.readFile();
    for (const data of db) {
      if (data.otp === otp) {
        return data;
      }
    }
  }

  fetch() {
    const db = this.readFile();
    return db.slice(-1)[0];
  }

  clear() {
    fs.writeFileSync(FileStorage.fileName, JSON.stringify([], null, 4));
  }
}

// export default FileStorage;
