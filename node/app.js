import express from "express";
import FileStorage from "./model.js";
import { fileURLToPath } from "url";
import { dirname } from "path";
import http from "http";
import { Server } from "socket.io";
import bodyParser from "body-parser";

const app = express();
const server = http.createServer(app);
const fileStorage = new FileStorage();
const io = new Server(server);

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

app.get("/", (req, res) => {
  res.sendFile(__dirname + "/index.html");
});

app.post("/parameters", (req, res) => {
  console.log(req.body);
  try {
    io.emit("message", req.body);
    fileStorage.saveData(req.body);
  } catch (error) {
    res
      .status(404)
      .json({ data: { err: "Problem inserting to file storage " + error } });
    return;
  }
  res.status(200).json({ data: { res: "success" } });
});

io.on("connection", (socket) => {
  console.log("A user connected");

  socket.on("message", (msg) => {
    // console.log("Message received:", msg);
    // Broadcast the message to all connected clients
    io.emit("message", msg);
  });

  socket.on("disconnect", () => {
    console.log("User disconnected");
  });
});

const PORT = process.env.PORT || 5000;
server.listen(PORT, "0.0.0.0", () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
