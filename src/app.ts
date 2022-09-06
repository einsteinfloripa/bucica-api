import express from "express";

import { presencaRouter } from "@routers";

const app = express();

app.get("/", (req, res) => res.send("Server is working"));

app.use("/presenca", presencaRouter);

export default app;
