
export async function POST(req: Request) {
    try {
        // need to wait the promise, cant just do settimeout or you get an error
        await new Promise((resolve) => setTimeout(resolve, 2 * 60000)); // Delay for 1 minute
        return new Response("Thanks for waiting");
    } catch (error) {
        // in case there are any errors
        console.error(error);
        return new Response("Sorry you could not wait", { status: 500 });
    }
}
