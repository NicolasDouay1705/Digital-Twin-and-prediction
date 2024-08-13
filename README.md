# Digital-Twin-and-prediction

Here is the repository of my 2e year internship.
I worked on a digital twin and prediction.

# How to use these code

The file Dashboard is two files: a dashboard code and the code of my digital twin class.
To use the digital twin, you have to follow this [tutorial](https://www.hivemq.com/blog/hands-on-guide-using-mqtt-hivemq-eclipse-ditto-digital-twins-iiot/) and add the following incoming payload mapping function to the right section:
'''

function mapToDittoProtocolMsg(headers, textPayload, bytePayload, contentType) {
    const jsonString = String.fromCharCode.apply(null, new Uint8Array(bytePayload));
    const jsonData = JSON.parse(jsonString); 
    const thingId = jsonData.thingId.split(':');
    const incomingHeaders = jsonData.header; 
    const replyTo = incomingHeaders["reply-to"] || "default-reply-topic";
    
    if (jsonData.command == "retrieve"){
        return Ditto.buildDittoProtocolMsg(
        thingId[0], // your namespace 
        thingId[1], 
        'things', // we deal with a thing
        'twin', // we want to update the twin
        'commands', // create a command to update the twin
        'retrieve', // modify the twin
        '/features', // modify all features at once
        {"reply-to": replyTo}
    );
    }
    if (jsonData.command == "modify"){
        const value = { 
        Voltage: { 
            properties: { 
                value: jsonData.voltage 
            } 
        },
        Current: { 
            properties: { 
                value: jsonData.current 
            } 
        }, 
		Capacity: { 
            properties: { 
                value: jsonData.capacity 
            } 
        },   
        };    
        return Ditto.buildDittoProtocolMsg(
            thingId[0], // your namespace 
            thingId[1], 
            'things', // we deal with a thing
            'twin', // we want to update the twin
            'commands', // create a command to update the twin
            'modify', // modify the twin
            '/features', // modify all features at once
            headers, 
            value
        );    
    }

}


'''

