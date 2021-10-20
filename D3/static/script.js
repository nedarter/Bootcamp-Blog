messages = [] 


function LoadMessages()
{
    d3.json("/loadmessages").then(response => {
        messages = response
        WriteMessages()
    })
}

function WriteMessages()
{
    console.log("Writing messages")
    messageDiv = d3.select("#messages")  
    messageDiv.html("")

    messages.forEach((x,index)=> {
        card = messageDiv.append("div")
        card.classed("card",true)

        card.append("div").classed("card-body", true)
                         .style("white-space", "pre-wrap")
                         .text(x.Message)
        card.append("div").classed("card-title", true).classed("card-footer",true)
                        .text(`${index + 1}) Posted By ${x.User} at ${x.PostTime}`)
                        
    });
}

function PostMessage()
{
    u = d3.select("#UserName").property("value")
    m = d3.select("#Message").property("value")

    d3.json("/postmessage",
        {
            method:"POST",
            body: JSON.stringify({
                "Message" : m,
                "UserName" : u
            }),
            headers: {
                "Content-Type": "application/json"
            }
        }).then(LoadMessages);
}

d3.select("#Submit").on("click", PostMessage)


LoadMessages()