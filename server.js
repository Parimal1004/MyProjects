const express = require("express");
const cors = require("cors");
const path = require("path");

const app = express();

app.use(express.json());
app.use(cors());

// ✅ Serve static files
app.use(express.static("public"));


// ================= FORCE LOGIN PAGE FIRST =================
app.get("/", (req, res) => {
    res.sendFile(path.join(__dirname, "public", "login.html"));
});


// ================= QUESTIONS =================
const questions = {

java:[
{
question:"Which keyword is used to inherit a class in Java?",
options:["this","super","extends","implements"],
answer:2
}, 
{
question:"Which method is entry point of Java program?",
options:["main()","start()","run()","init()"],
answer:0
},
{
question:"Java is?",
options:["Compiled","Interpreted","Both","None"],
answer:2
},
{
question:"Which package contains Scanner class?",
options:["java.io","java.util","java.lang","java.awt"],
answer:1
},
{
question:"Which keyword is used to create object?",
options:["new","class","this","void"],
answer:0
},
{
question:"Which datatype is 32-bit?",
options:["int","long","byte","double"],
answer:0
},
{
question:"Which concept allows same method name?",
options:["Inheritance","Encapsulation","Polymorphism","Abstraction"],
answer:2
},
{
question:"Which keyword prevents inheritance?",
options:["static","const","final","private"],
answer:2
},
{
question:"Which keyword is used to import package?",
options:["include","import","package","using"],
answer:1
},
{
question:"Which exception occurs when divide by zero?",
options:["NullPointer","ArithmeticException","IOException","NumberFormat"],
answer:1
}
],

python:[
{
question:"Which symbol is used for comments in Python?",
options:["//","#","/*","--"],
answer:1
},
{
question:"Which datatype is immutable?",
options:["list","set","tuple","dict"],
answer:2
},
{
question:"Which keyword defines function?",
options:["function","def","fun","define"],
answer:1
},
{
question:"Which operator is exponent?",
options:["^","**","//","%"],
answer:1
},
{
question:"Which keyword used for loop?",
options:["loop","iterate","for","repeat"],
answer:2
},
{
question:"Which data structure stores key-value?",
options:["list","tuple","dict","set"],
answer:2
},
{
question:"Which keyword handles exception?",
options:["try","catch","handle","check"],
answer:0
},
{
question:"Which function prints output?",
options:["echo()","display()","print()","show()"],
answer:2
},
{
question:"Which keyword creates class?",
options:["class","define","struct","object"],
answer:0
},
{
question:"Which operator is used for division?",
options:["/","//","%","**"],
answer:0
}
],

dsa:[
{
question:"Which DS uses FIFO?",
options:["Stack","Queue","Tree","Graph"],
answer:1
},
{
question:"Which DS uses LIFO?",
options:["Stack","Queue","Array","Tree"],
answer:0
},
{
question:"Binary search works on?",
options:["Sorted array","Unsorted array","Graph","Tree"],
answer:0
},
{
question:"Which DS stores elements in nodes?",
options:["Array","Linked List","Stack","Queue"],
answer:1
},
{
question:"Which traversal uses root-left-right?",
options:["Inorder","Preorder","Postorder","Level"],
answer:1
},
{
question:"Time complexity of binary search?",
options:["O(n)","O(log n)","O(n2)","O(1)"],
answer:1
},
{
question:"Which DS uses push and pop?",
options:["Queue","Stack","Tree","Graph"],
answer:1
},
{
question:"Graph consists of?",
options:["Nodes & edges","Arrays","Stacks","Queues"],
answer:0
},
{
question:"Which algorithm finds shortest path?",
options:["DFS","BFS","Dijkstra","Sorting"],
answer:2
},
{
question:"Which structure is hierarchical?",
options:["Array","Tree","Queue","Stack"],
answer:1
}
],

html:[
{
question:"HTML stands for?",
options:[
"Hyper Text Markup Language",
"High Text Machine Language",
"Hyperlinks Text Mark Language",
"None"
],
answer:0
},
{
question:"Which tag creates hyperlink?",
options:["a","link","href","hyper"],
answer:0
},
{
question:"Which tag inserts image?",
options:["img","image","pic","src"],
answer:0
},
{
question:"CSS stands for?",
options:[
"Cascading Style Sheets",
"Creative Style Sheet",
"Computer Style Sheet",
"Color Style Sheet"
],
answer:0
},
{
question:"Which property changes text color?",
options:["font-color","text-color","color","bgcolor"],
answer:2
},
{
question:"Which tag creates paragraph?",
options:["p","para","text","br"],
answer:0
},
{
question:"Which tag creates table?",
options:["table","tab","tr","td"],
answer:0
},
{
question:"Which CSS property changes background?",
options:["bgcolor","background","color","back"],
answer:1
},
{
question:"Which tag creates heading?",
options:["h1","head","title","heading"],
answer:0
},
{
question:"Which CSS property changes font size?",
options:["font-style","font-size","text-size","size"],
answer:1
}
]

};


// ================= API =================

// ✅ GET QUESTIONS
app.get("/questions/:subject", (req, res) => {
    const subject = req.params.subject;

    if(!questions[subject]){
        return res.status(404).json({ error: "Invalid subject" });
    }

    res.json(questions[subject]);
});


// ✅ SUBMIT ANSWERS
app.post("/submit/:subject", (req, res) => {

    const subject = req.params.subject;
    const { answers } = req.body;

    if(!questions[subject]){
        return res.status(404).json({ error: "Invalid subject" });
    }

    let score = 0;

    questions[subject].forEach((q, i) => {
        if (q.answer === answers[i]) score++;
    });

    res.json({
        score,
        total: questions[subject].length
    });
});


// ================= SERVER =================
app.listen(3000, () => {
    console.log("Server running on http://localhost:3000");
});