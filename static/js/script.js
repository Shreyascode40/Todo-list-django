// side clock

function updateClock() {
            const now = new Date();
            
            // Get time components
            const hours = now.getHours();
            const minutes = now.getMinutes();
            const seconds = now.getSeconds();
            
            // Update analog clock
            const secondDeg = (seconds / 60) * 360;
            const minuteDeg = ((minutes + seconds / 60) / 60) * 360;
            const hourDeg = ((hours % 12 + minutes / 60) / 12) * 360;
            
            document.getElementById('secondHand').style.transform = `rotate(${secondDeg}deg)`;
            document.getElementById('minuteHand').style.transform = `rotate(${minuteDeg}deg)`;
            document.getElementById('hourHand').style.transform = `rotate(${hourDeg}deg)`;
            
            // Update digital clock
            const timeString = `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
            document.getElementById('time').textContent = timeString;
            
            // Update date
            const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
            const dateString = now.toLocaleDateString('en-US', options);
            document.getElementById('date').textContent = dateString;
        }
        
        // Update immediately and then every second
        updateClock();
        setInterval(updateClock, 1000);
        console.log("JS connected successfully!");



// task animation 
new Chart(document.getElementById('yearChart'), {
    type: 'bar',
    data: {
        labels: JSON.parse(document.getElementById('yearChart').dataset.months),
        datasets:[{
            label: `Tasks Completed in ${document.getElementById('yearChart').dataset.year}`,
            data: JSON.parse(document.getElementById('yearChart').dataset.counts),
            backgroundColor: '#ff7a18'
        }]
    },
    options: {
        scales: {
            y: { beginAtZero: true }
        }
    }
});
