const eventBox = document.getElementById('event-box')
const countDownBox = document.getElementById('countdown-box')

// console.log(eventBox.textContent)
const eventDate = Date.parse(eventBox.textContent)
// console.log(eventDate)

const myCount = setInterval(()=>{
    const now = new Date().getTime()
    // console.log(now)

    const diff = eventDate - now
    // console.log(diff)

    const days = Math.floor(eventDate / (1000 * 60 * 60 * 24) - (now / (1000 * 60 * 60 * 24)));
    // console.log(days)
    const hours = Math.floor((eventDate / (1000 * 60 * 60) - (now / (1000 * 60 * 60))) % 24);
    // console.log(hours)
    const minutes = Math.floor((eventDate / (1000 * 60) - (now / (1000 * 60))) % 60);
    // console.log(minutes)
    const seconds = Math.floor((eventDate / (1000) - (now / (1000))) % 60);
    // console.log(seconds)

    if (diff > 0){
        countDownBox.innerHTML = days + ' days,' + hours + ' hours,' + minutes + ' minutes,' + seconds + ' seconds.'
    }else{
        clearInterval(myCount)
        countDownBox.innerHTML = 'Meeting is Overdue'
    }
 
}, 1000)



