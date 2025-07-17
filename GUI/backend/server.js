const express = require("express");
const path = require("path");
const http = require("http");

const app = express();


// Storing the game state
let gameState = null;

app.get("/", (req, res) => {
    res.sendFile(path.join(__dirname, '../Q_TicTacToe.html'));
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
})

app.get("/api/game-state", (req, res) => {
    if (gameState) {
        res.json(gameState);
    } else {
        res.status(503).json({error: "Game state not available"});
    }
});

app.post("/api/update-game-state", (req, res) => {
    fetchGameState();
    res.json({ message: "Game state updated successfully." });
});

function fetchGameState() {
    http.get("http://localhost:5000/api/game-state", (res) => {
        let data = "";

        res.on("data", (chunk) => {
            data += chunk;
        });

        res.on("end", () => {
            try {
                const jsonData = JSON.parse(data);
                gameState = jsonData;
            }
            catch (error) {
                console.error("Error parsing JSON:", error);
            }
        });
    }).on("error", (err) => {
        console.error("Error fetching data:", err);
    });
}
