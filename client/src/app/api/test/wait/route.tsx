
export async function POST(req: Request) {
    try {
        // need to wait the promise, cant just do settimeout or you get an error
        await new Promise((resolve) => setTimeout(resolve, 1 * 60000)); // Delay for 1 minute
        return new Response(JSON.stringify({message:"Thanks for waiting"}), {status:200});
    } catch (error) {
        // in case there are any errors
        console.error(error);
        return new Response(JSON.stringify({error:"Sorry you could not wait"}), { status: 500 });
    }
}
