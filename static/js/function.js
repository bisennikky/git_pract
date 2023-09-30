function updateCurrentDate() {
    const currentDate = new Date();
    const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    const formattedDate = currentDate.toLocaleDateString(undefined, options);
    document.getElementById("currentDateSpan").textContent = formattedDate;
}

// Call the function initially and then update the date as needed
updateCurrentDate();

function updateCurrentTime() {
    const currentDate = new Date();
    const hours = currentDate.getHours();
    const minutes = currentDate.getMinutes();
    const amPM = hours >= 12 ? 'PM' : 'AM';
    const formattedTime = `${(hours % 12 === 0 ? 12 : hours % 12)}:${minutes.toString().padStart(2, '0')} ${amPM}`;
    document.getElementById("currentTimeSpan").textContent = formattedTime;
}

// Call the function initially and then update the time every minute
updateCurrentTime();
setInterval(updateCurrentTime, 60000);



var ip 
function ip_func(){
    fetch("../static/js/ip.json")
    .then((res) => {
    return res.json();
})
.then((data) => {console.log(data.ip);
    ip = data.ip+'/test';
    ;});
}
ip_func()

let serial_no = { ID: "EVZ_DPTH_02/status" };

function display(data1) {
    console.log('_____data1____', data1);
    document.getElementById("temp").innerHTML = parseFloat(data1.temp).toFixed(1);
    document.getElementById("hum").innerHTML = parseFloat(data1.hum).toFixed(0);
    document.getElementById("dp").innerHTML = parseFloat(data1.dp).toFixed(0);
}

async function send() {
    try {
        // Use the 'ip' variable obtained from the ip_func function
        const response = await fetch(ip, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(serial_no),
        });

        if (response.ok) {
            const contentType = response.headers.get('content-type');
            if (contentType && contentType.includes('application/json')) {
                const data = await response.json();
                display(data);
            } else {
                console.log('Response is not in JSON format');
            }
        } else {
            throw new Error('Network response was not ok.');
        }
    } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
    }
}

var s_data = setInterval(send, 5000);