document.addEventListener("DOMContentLoaded", () => {
    const startGameButton = document.getElementById("start-game");
    const resetGameButton = document.getElementById("reset-game");
    const liveButton = document.getElementById("mark-live");
    const blankButton = document.getElementById("mark-blank");
    const errorMessage = document.getElementById("error-message");

    startGameButton.addEventListener("click", () => {
        const blanks = parseInt(document.getElementById("blanks").value) || 0;
        const lives = parseInt(document.getElementById("lives").value) || 0;
        const total = blanks + lives;

        fetch("/start", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ total_shells: total, live_shells: lives, blank_shells: blanks }),
        })
            .then((response) => {
                if (!response.ok) {
                    return response.json().then((data) => {
                        throw new Error(data.message);
                    });
                }
                return response.json();
            })
            .then((data) => {
                updateTracker(data.game_state);
                errorMessage.innerText = ""; // Clear error message on success
            })
            .catch((error) => {
                errorMessage.innerText = error.message; // Display error message
            });
    });

    resetGameButton.addEventListener("click", () => {
        fetch("/reset", { method: "POST" })
            .then((response) => response.json())
            .then(() => {
                // Clear the tracker
                updateTracker({ total_shells: 0, live_shells: 0, blank_shells: 0, shells: [] });
                errorMessage.innerText = ""; // Clear error message on reset
    
                // Clear the input boxes
                document.getElementById("blanks").value = "";
                document.getElementById("lives").value = "";
            });
    });
    
    liveButton.addEventListener("click", () => configureShell("live"));
    blankButton.addEventListener("click", () => configureShell("blank"));

    function updateTracker(gameState) {
        document.getElementById("total-shells").innerText = gameState.total_shells;
        document.getElementById("live-shells").innerText = gameState.live_shells;
        document.getElementById("blank-shells").innerText = gameState.blank_shells;

        const shellsContainer = document.getElementById("shells");
        shellsContainer.innerHTML = "";
        gameState.shells.forEach((shell, index) => {
            const shellElement = document.createElement("div");
            shellElement.classList.add("shell", shell);
            shellElement.innerText = index + 1;
            shellElement.addEventListener("click", () => selectShell(index));
            shellsContainer.appendChild(shellElement);
        });

        const probLive = (gameState.live_shells / gameState.total_shells) * 100 || 0;
        const probBlank = (gameState.blank_shells / gameState.total_shells) * 100 || 0;

        document.getElementById("prob-live").innerText = `${probLive.toFixed(1)}%`;
        document.getElementById("prob-blank").innerText = `${probBlank.toFixed(1)}%`;
    }

    function selectShell(index) {
        fetch("/select", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ index: index }),
        })
            .then((response) => response.json())
            .then(() => {
                // Highlight the selected shell
                const shellsContainer = document.getElementById("shells");
                Array.from(shellsContainer.children).forEach((shell, idx) => {
                    if (idx === index) {
                        shell.classList.add("selected");
                    } else {
                        shell.classList.remove("selected");
                    }
                });
    
                console.log(`Shell ${index + 1} selected`);
            });
    }
    

    const clearShellButton = document.getElementById("clear-shell");

    clearShellButton.addEventListener("click", () => {
        clearShell();
    });

    function clearShell() {
        fetch('/clear', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({})
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.message);
            } else {
                // Update the UI with the cleared game state
                updateTracker(data.game_state);
            }
        })
        .catch(err => console.error('Error clearing shell:', err));
    }
    
    

    function configureShell(type) {
        fetch("/configure", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ type: type }),
        })
            .then((response) => response.json())
            .then((data) => {
                updateTracker(data.game_state);
            });
    }



    window.focusLives = function () {
        const blanksInput = document.getElementById("blanks");
        const livesInput = document.getElementById("lives");
    
        if (blanksInput.value !== "") {
            livesInput.focus();
        }
    };
    
    window.focusBlanks = function () {
        const blanksInput = document.getElementById("blanks");
        const livesInput = document.getElementById("lives");
    
        if (livesInput.value !== "") {
            blanksInput.focus();
        }
    };
    

    
});


