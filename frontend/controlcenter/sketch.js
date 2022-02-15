// All in cm
const gridSize = 5; // How much numbers are rounded by
const gridCellResolution = 4; // How many px to draw a cell as
const arenaWidth = 500;
const arenaHeight = 1500;
const robotWidth = 10;
const robotHeight = 39;

let ws, xws;
let driveSettings, generalSettings, consoleSettings;
let state = 2; // 0 = TD, 1 = AD, 2 = AI
const states = ["Tank Drive", "Arcade Drive", "Autonomous"];
const shortStates = ["TD", "AD", "AI"];

// Messages received over WebSocket
let msgs = [];

// Last received robot and obstacle locations
let obstacles = []; // [{x, y}, {x, y}, ...]
let robot = {x: arenaWidth / 2, y: 1.5 * robotHeight, a: 0}; // a is angle

// UI components
let panels = [];

function setup() {
	// ws = {send: console.log};

	const ip = prompt("What IP is robot on?", "192.168.2.49");
	const port = prompt("What port number is the robot using?", "8080")
	console.log(`Connecting to ws://${ip}:${port}`)
	ws = new WebSocket(`ws://${ip}:${port}`);
	ws.onmessage = gotMessage;

	ws.onclose = msg => {
		alert("Websocket connection closed. Please refresh the webpage to reconnect.");
		console.log(msg, /CLOSE/);
	};

	ws.onerror = msg => {
		console.log(msg, /ERROR/);
	};

	// xbox server WebSocket
	// xws = new WebSocket("ws://localhost:8001");
	// xws.onmessage = xboxServerRecv;
	// xws.onclose = msg => {
	// 	alert("lost connection with the xbox sever... referesh to reconnect");
	// };

	driveSettings = QuickSettings.create(document.body.clientWidth - 300, 0.4 * document.body.clientHeight, "Drive settings")
		.addButton("Tank Drive", () => handlePress("TD"))
		.addButton("Arcade Drive",() => handlePress("AD"))
		.addButton("Autonomous", () => handlePress("AI"))
		.addButton("STOP", () => handlePress("STOP"))
		.addButton("CLEAROBS", clearObstacles)
		.overrideStyle("STOP", "backgroundColor", "red")
		.overrideStyle("STOP", "color", "white")
		.setWidth(200)
		.setHeight(225);

	for (let state of states) {
		driveSettings.overrideStyle(state, "backgroundColor", "gray");
	}

	driveSettings.overrideStyle(states[state], "backgroundColor", "green");

	//
	generalSettings = QuickSettings.create(document.body.clientWidth - 300, 0.4 * document.body.clientHeight + 250, "General settings")
		.addBoolean("Snap panels right", true, window.onresize)
		.addRange("Controller refresh (ms)", 100, 5000, 1500, 100)
		.setWidth(200)
		.setHeight(150)

	// some logging
	consoleSettings = QuickSettings.create(document.body.clientWidth - 300, 0.4 * document.body.clientHeight + 425, "Console")
		.addTextArea("Output")
		.overrideStyle("Output", "backgroundColor", "black")
		.overrideStyle("Output", "color", "white")
		.setWidth(350)
		.setHeight(150)
		.disableControl("Output");

	panels = [ generalSettings, driveSettings, consoleSettings ];
	createCanvas(arenaWidth * gridCellResolution / gridSize, arenaHeight * gridCellResolution / gridSize);
	frameRate(10);
	angleMode(DEGREES);
	rectMode(CENTER);
	console.log(CENTER, "CENTER");
	window.onresize();
	sendState();
}

let cmdQueue = [];
function xboxServerRecv(msg) {
	console.log(`Got message: ${msg.data}`);
	const cmd = msg.data.split(':');
	if (cmd.length < 2)
		return;


	if (msg[0] == "a") {

	}
}

// Changes mode when someone clicks the button
function handlePress(name) {
	if (name === "STOP") {
		handleStateChange(state, -1);
		return send("STOP");
	}

	let newState = shortStates.indexOf(name) === -1 ? state : shortStates.indexOf(name);
	if (newState === state) return;

	handleStateChange(state, newState);

	if (newState < 2) {
		return sendXBOX(name);
	} else if (newState === 2) {
		return send(name);
	}
}

function clearObstacles() {
	obstacles = [];
}

async function emptyQueue() {
	cmdQueue.forEach((e, i) => {
		send(e[0], e[1]);
	});
	cmdQueue = [];
}

// Async loop to send Arcade/Tank Drive commands
async function sendState() {
	if (state >= 0 && state < 2) {
		await sendXBOX(states[state].split(" ").map(n => n[0]).join(""));
	}

	emptyQueue()

	// sleep function
	await new Promise(next => setTimeout(next, generalSettings.getValue("Controller refresh (ms)")));
	sendState();
}


// Changes color of buttons
function handleStateChange(oldState, newState) {
	driveSettings.overrideStyle(states[oldState], "backgroundColor", "gray");
	if (newState >= 0) driveSettings.overrideStyle(states[newState], "backgroundColor", "green");
	state = newState;
}


// Makes the appropriate requests for Arcade/Tank Drive
async function sendXBOX(name) {
	let ret = {};
	try {
		let leftY = await (await fetch("http://localhost:3000/leftY")).json();

		if (name === "AD") {
			leftX = await (await fetch("http://localhost:3000/leftX")).json();
			return send("AD", `${leftY},${leftX}`);
		} else {
			let right = await (await fetch("http://localhost:3000/rightX")).json();
			return send("TD", `${leftY},${right}`);
		}
	} catch(e) {
		console.log("Error in requesting XBOX:", e);
	}
}

// Send data over WebSocket
async function send(name, data) {
	if (data) {
		outputConsole(`${name}:${data}`);
		return ws.send(`${name}:${data}`);
	}

	else {
		outputConsole(name)
		return ws.send(name);
	}
}


// Output to console on webpage
function outputConsole(output) {
	let prevOutput = consoleSettings.getValue("Output");
	let rightNow = new Date();

	// Time components must be 2 digits
	const pad = n => n < 10 ? '0' + n : n;

	// > Output Text (hh:mm:ss)
	consoleSettings.setValue("Output", `${prevOutput}\n> ${output} (${pad(rightNow.getHours())}:${pad(rightNow.getMinutes())}:${pad(rightNow.getSeconds())})`);
	let outputElem = document.getElementById("Output");
	outputElem.scrollTop = outputElem.scrollHeight;
}

// Normalize x -> take gridded value to pixel value
function nX(x) {
	return width - Math.floor(Number(x) / gridSize) * gridCellResolution;
}

// Normalize y -> Canvas draws things from bottom to top so flip the y value
function nY(y) {
	return height -  Math.floor(Number(y) / gridSize) * gridCellResolution;
}

// Draw map
function draw() {
	background(81);

	// Draw robot
	fill("#AEAEAE");
	strokeWeight(3);
	stroke(0);
	push();
	translate(nX(robot.x), nY(robot.y));
	rotate(degrees(robot.a));
	rect(0, 0, robotWidth, robotHeight); // Actual robot
	fill("#343434");
	rect(0, -robotHeight / 2, robotWidth / 2, robotWidth / 2); // Directional head / Obstacle Lidar
	pop();

	// Draw obstacles
	push();
	strokeWeight(1);
	stroke(50);
	fill("#FFFFFF");
	rectMode(CORNER);	
	for (const o of obstacles) {
		// const o = obstacles[i];
		rect(nX(o.x), nY(o.y), gridCellResolution, gridCellResolution);
	}
	
	pop();
}

// WebSocket received message
function gotMessage(msg) {
	if (msg.data.indexOf(":") === -1) {
		msgs.push(msg.data);
		return console.log(`Unknown message format: ${msg.data}`);
	}
	let args = msg.data.split(":");
	let command = args[0];
	let data = args[1].split(",");

	if (command === "R") {
		let [x, y, a] = data;
		robot = {x, y, a, time: Date.now()};
		outputConsole(`RobotPos: (${x},${y}, ${a})`)
	} else if (command === "O") {
		// outputConsole(`Obstacles: ${data}`);
		obstacles = [];
		for (let i = 0; i < data.length; i+=2) {
			try {
				let [x, y] = data.slice(i, i + 2);
				obstacles.push({x, y, time: Date.now()});
			} catch (e) {}
		}
	} else if (command === "M") {
		let msg = args[1];
		outputConsole(`Message: ${msg}`)
	} else console.log(`Unknown command: ${msg.data}`);
	msgs.push(msg.data);
}

// Auto-move panels on resize
window.onresize = function (event) {
	if (!generalSettings.getValue("Snap panels right")) {
		return;
	}
	for (const panel of panels) {
		let curY = parseInt(panel._panel.style.top.split("px")[0]);
		let curWidth = parseInt(panel._panel.style.width.split("px")[0]);
		panel.setPosition(document.body.clientWidth - curWidth - 50, curY);
	}
};
