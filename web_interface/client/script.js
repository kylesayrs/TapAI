import { io } from "socket.io-client";

const roleInput = document.getElementById("role");
const joinQueueButton = document.getElementById("jq");
const leaveQueueButton = document.getElementById("lq");
const homePage = document.getElementById("home");
const queuePage = document.getElementById("in_queue");

const gameStartedGuesserPage = document.getElementById("game_started_guesser");
const gameStartedDescriberPage = document.getElementById("game_started_describer");

const submitDescriptionButton = document.getElementById("sd");
const descriptionInput = document.getElementById("description");
const choiceInput = document.getElementById("choice");

const guessPhaseDescriberPage = document.getElementById("guess_phase_describer");
const guessPhaseGuesserPage = document.getElementById("guess_phase_guesser");
const textDescription = document.getElementById("given_description");
const guessInput = document.getElementById("guess");

const submitGuessButton = document.getElementById("sg");
const resultsPage = document.getElementById("game_results");

const gameDescription = document.getElementById("game_description");
const gameGuess = document.getElementById("game_guess");
const gameAIGuess = document.getElementById("ai_guess");
const gameAnimal = document.getElementById("game_animal");
const gameResult = document.getElementById("result");

const socket = io("http://localhost:3000");
socket.on("connect", () => {
    console.log(`Connected to server with id: ${socket.id}`);
});

socket.on("gameStarted", game => {
    console.log(game);
    homePage.style.display = "none";
    queuePage.style.display = "none";

    let self = game.players.find(e => e.id === socket.id);
    if (self.role === "guesser") {
        gameStartedGuesserPage.style.display = "block";
        socket.on("description", game => {
            // check if one of the players is self
            let self = game.players.find(e => e.id === socket.id);
            if (self) {
                gameStartedGuesserPage.style.display = "none";
                guessPhaseGuesserPage.style.display = "block";
                textDescription.innerHTML = game.description;
            }
        });
    } else {
        gameStartedDescriberPage.style.display = "block";
    }
});

socket.on("guessSubmitted", game => {
    console.log("guess submitted");
    // check if we are a player in the game
    let self = game.players.find(e => e.id === socket.id);
    if (self) {
        guessPhaseGuesserPage.style.display = "none";
        guessPhaseDescriberPage.style.display = "none";
        resultsPage.style.display = "block";
        gameDescription.innerHTML = game.description;
        gameGuess.innerHTML = game.choice;
        gameAIGuess.innerHTML = game.ai_guess;
        gameAnimal.innerHTML = game.player_guess;
        gameResult.innerHTML = game.choice === game.player_guess ? "You win!" : "You lose!";
    }
});

submitGuessButton.addEventListener("click", () => {
    let guess = guessInput.value;
    socket.emit("submitGuess", { id: socket.id, guess: guess});
});



const joinQueue = (role) => {
    socket.emit("joinQueue", { id: socket.id, role: role }, queueJoined);
}

const leaveQueue = () => {
    socket.emit("leaveQueue", { id: socket.id }, queueLeft);
}

joinQueueButton.addEventListener("click", () => {
    joinQueue(roleInput.value);
});

leaveQueueButton.addEventListener("click", () => {  
    leaveQueue();
});

submitDescriptionButton.addEventListener("click", () => {
    socket.emit("submitDescription", { id: socket.id, description: descriptionInput.value, choice: choiceInput.value }, descriptionSubmitted);
});

/* queueJoined
 * purpose: switch to queue page when player joins queue successfully
 */
const queueJoined = () => {
    homePage.style.display = "none";
    queuePage.style.display = "block";
}

/* queueLeft
* purpose: switch to home page when player leaves queue successfully
*/
const queueLeft = () => {
    homePage.style.display = "block";
    queuePage.style.display = "none";
}

const descriptionSubmitted = () => {
    gameStartedDescriberPage.style.display = "none";
    guessPhaseDescriberPage.style.display = "block";
}