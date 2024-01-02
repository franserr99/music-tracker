// src/styles/globals.d.ts
import { Connection, Mongoose } from "mongoose";

declare global {
  var mongoose: {
    conn: Connection | null,
    promise: Promise<Mongoose> | null
  }
}
