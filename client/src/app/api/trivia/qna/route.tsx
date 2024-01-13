
import mdbConnect from "@/util/mongoConnect";
import TriviaCardModel, { ITriviaCard } from "@/models/TriviaCardModel";
import { NextRequest } from "next/server";

// define type for request
type ResponseData = ITriviaCard[];

type ApiResponse<T> = {
    data?: T | undefined;
    error?: string  | undefined;
};

export async function GET(request: NextRequest) {


    try {
        await mdbConnect();
        const data = await TriviaCardModel.find() as ResponseData;
        // return new Response({data}, { status: 200 }).json()
        return new Response (JSON.stringify(data), {status:200})
    } catch (err) {
        console.log("Error:", err);
        return new Response (JSON.stringify({error:"Could not fetch data."}),{status:400})
        // return new Response ({error:"Could not fetch data"}, {status:500})
    }

}
