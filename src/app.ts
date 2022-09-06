import express from "express";
import "express-async-errors";

import { presencaRouter } from "@routers";
import { errorHandlerMiddleware } from "@middlewares";

const app = express();

app.get("/", (req, res) => res.send("Server is working"));

app.use("/presenca", presencaRouter);
app.use(errorHandlerMiddleware);

export default app;
