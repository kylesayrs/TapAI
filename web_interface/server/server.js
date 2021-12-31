const io = require("socket.io")(3000, {
    cors: {
        origin: ["http://localhost:8080"]
    }
})

let queue = []
let games = []

io.on("connection", socket => {
    io.emit("queue", queue)
    console.log(socket.id)

    /* join queue allows players to join the queue
    *  if the queue is joined successfully, the player is added to the queue
    *  and a callback is sent to the client
    */
    socket.on("joinQueue", (data, cb) => {
        if (!data.id) {
            console.log("No id")
        } else if (queue.some(e => e.id === socket.id)) {
            console.log("Already in queue")
        } else {
            queue.push(data)
            

            /* check queue for 2 people with the same role */
            if (queue.filter(e => e.role !== data.role).length >= 1) {
                /* if there are 2 people with the same role, create a game */
                let players = queue.filter(e => e.role !== data.role)
                players.push(data)
                let game = {
                    players: players,
                    description: "",
                    choice: "",
                    player_guess: "",
                    ai_guess: ""
                }
                console.log("players: ", players)
                games.push(game)
                queue.pop(players[0])
                queue.pop(players[1])
                cb()
                /* send game to client */
                setTimeout(() => {
                    io.emit("gameStarted", game)
                }, 1000)
            } else {
                cb()
            }


            console.log(queue)
        }
    })

    /* leave queue allows players to leave the queue
    *  if the queue is left successfully, the player is removed from the queue
    *  and a callback is sent to the client
    */
    socket.on("leaveQueue", (data, cb) => {
        if (!data.id) {
            console.log("No id")
        } else if (!queue.some(e => e.id === socket.id)) {
            console.log("Not in queue")
        } else {
            queue = queue.filter(e => e.id !== socket.id)
            io.emit("queueUpdate", queue)   
            cb()    
        }
    })

    /* give description allows players to give a description to the game */
    socket.on("submitDescription", (data, cb) => {
        if (!data.id) {
            console.log("No id")
        } else if (!games.some(e => e.players.some(e => e.id === socket.id))) {
            console.log("Not in game")
        } else if (!data.description) {
            console.log("No description")
        } else {
            let game = games.find(e => e.players.some(e => e.id === socket.id))
            game.description = data.description
            game.choice = data.choice
            
            /* call python script to create ai guess */
            console.log("running python script")

            let spawn = require("child_process").spawn

            /* todo: figure out how to change this to relative file path */
            let pythonProcess = spawn('/Users/jimmymaslen/opt/miniconda3/envs/ml135_env_sp21/bin/python', ["/Users/jimmymaslen/Documents/GitHub/TapAI/make_guess.py", game.description])

            pythonProcess.stdout.on('data', function(data) {
                game.ai_guess = data.toString()
                console.log(game.ai_guess)
            })
            pythonProcess.stderr.on('data', function(data) {
                console.log(data.toString())
            })

            /* broadcast description to both players */
            io.emit("description", game)
            cb()
        }
    })

    /* submit guess allows players to submit a guess to the game */
    socket.on("submitGuess", data => {
        if (!data.id) {
            console.log("No id")
        } else if (!games.some(e => e.players.some(e => e.id === socket.id))) {
            console.log("Not in game")
        } else if (!data.guess) {
            console.log("No guess")
        } else {
            let game = games.find(e => e.players.some(e => e.id === socket.id))
            game.player_guess = data.guess
            /* broudcase guess to both players */
            console.log(game.ai_guess)
            io.emit("guessSubmitted", game)
        }
    })
})