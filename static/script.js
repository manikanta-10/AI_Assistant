async function generateResponse() {

    const selectedFunction =
        document.getElementById("function").value;

    const userInput =
        document.getElementById("userInput").value;

    document.getElementById("responseBox").innerHTML =
        "<h3>🤖 AI is thinking...</h3>";

    const response =
        await fetch("/generate", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                function_name: selectedFunction,
                user_input: userInput
            })
        });

    const data = await response.json();

    document.getElementById("responseBox").innerHTML =
        data.response;
}
async function sendFeedback(feedback) {

    await fetch("/feedback", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            feedback: feedback
        })
    });

    alert("Thank you for your feedback!");
}