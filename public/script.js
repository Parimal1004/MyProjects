let answers = [];
let time = 60;
let totalTime = 60;
let submitted = false;

const subject = localStorage.getItem("subject");
let questions = [];

if (!subject) {
    alert("Please select subject first");
    window.location.href = "subjects.html";
}

// ================= LOAD QUESTIONS =================

fetch(`/questions/${subject}`)
.then(res => res.json())
.then(data => {

    questions = data;

    const form = document.getElementById("examForm");
    form.innerHTML = "";

    data.forEach((q, i) => {

        let html = `
        <div class="question-box" id="q${i}">
        <p><b>${i + 1}. ${q.question}</b></p>
        `;

        q.options.forEach((opt, j) => {

            html += `
            <label id="q${i}opt${j}">
            <input type="radio"
            name="q${i}"
            value="${j}"
            onchange="answers[${i}] = ${j}">
            ${opt}
            </label><br>
            `;
        });

        html += "</div>";

        form.innerHTML += html;
    });

})
.catch(err => console.log(err));


// ================= TIMER =================

let timer = setInterval(() => {

    if (submitted) return;

    time--;

    document.getElementById("timer").innerText = "Time: " + time;

    let percent = (time / totalTime) * 100;
    document.getElementById("progressBar").style.width = percent + "%";

    if (time <= 20) {
        document.getElementById("progressBar").style.background = "red";
    }
    else if (time <= 40) {
        document.getElementById("progressBar").style.background = "orange";
    }

    if (time === 0) {
        clearInterval(timer);
        submitExam();
    }

}, 1000);


// ================= SUBMIT =================

function submitExam(){

    if(submitted) return;

    submitted = true;
    clearInterval(timer);

    fetch(`/submit/${subject}`, {
        method:"POST",
        headers:{ "Content-Type":"application/json" },
        body: JSON.stringify({ answers })
    })
    .then(res=>res.json())
    .then(data=>{

        // store data for result page
        localStorage.setItem("lastAnswers", JSON.stringify(answers));
        localStorage.setItem("lastQuestions", JSON.stringify(questions));
        localStorage.setItem("lastScore", data.score);
        localStorage.setItem("lastTotal", data.total);

        window.location.href = "result.html";
    });
}


// ================= HIGHLIGHT ANSWERS =================

function highlightAnswers(){

    questions.forEach((q, i) => {

        q.options.forEach((opt, j) => {

            let option = document.getElementById(`q${i}opt${j}`);

            if (q.answer === j) {
                option.style.background = "green";
                option.style.color = "white";
            }

            if (answers[i] == j && q.answer !== j) {
                option.style.background = "red";
                option.style.color = "white";
            }
        });
    });

}


// ================= RESULT POPUP =================

function showResultPopup(score, total, percentage, grade){

    const popup = document.createElement("div");

    popup.innerHTML = `
    <div style="
    position:fixed;
    top:0; left:0;
    width:100%; height:100%;
    background:rgba(0,0,0,0.6);
    display:flex;
    justify-content:center;
    align-items:center;
    ">

    <div style="
    background:white;
    padding:25px;
    border-radius:12px;
    text-align:center;
    width:300px;
    ">

    <h2>Result</h2>

    <p><b>Score:</b> ${score} / ${total}</p>
    <p><b>Percentage:</b> ${percentage}%</p>
    <p><b>Grade:</b> ${grade}</p>

    <button onclick="window.location.href='subjects.html'">
    Back to Subjects
    </button>

    </div>  
    </div>
    `;

    document.body.appendChild(popup);
}