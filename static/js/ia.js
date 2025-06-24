const chat = document.querySelector(".chat");
const input = document.getElementById("messageInput");

function sendMessage() {
  const message = input.value.trim();
  if (message === "") return;

  // Cria o wrapper para a mensagem do usuário e o emoji
  const userMessageWrapper = document.createElement("div");
  userMessageWrapper.classList.add("message-wrapper", "user-wrapper");

  // Cria a div para o texto da mensagem do usuário
  const userMessageText = document.createElement("div");
  userMessageText.classList.add("message", "user");
  userMessageText.textContent = message; // Apenas o texto aqui

  // Cria o span para o emoji do professor
  const userEmoji = document.createElement("span");
  userEmoji.classList.add("message-emoji");
  userEmoji.textContent = "🧑‍🏫";

  // Adiciona o texto e o emoji ao wrapper do usuário
  userMessageWrapper.appendChild(userMessageText);
  userMessageWrapper.appendChild(userEmoji);
  chat.appendChild(userMessageWrapper);

  input.value = "";
  chat.scrollTop = chat.scrollHeight;

  // Resposta simulada da IA com emoji de robô
  setTimeout(() => {
    // Cria o wrapper para a mensagem do bot e o emoji
    const botMessageWrapper = document.createElement("div");
    botMessageWrapper.classList.add("message-wrapper", "bot-wrapper");

    const botEmoji = document.createElement("span");
    botEmoji.textContent = "🤖";
    botEmoji.classList.add("message-emoji");

    // Cria a div para o texto da mensagem do bot
    const botMessageText = document.createElement("div");
    botMessageText.classList.add("message", "bot");
    botMessageText.textContent = `Recebi sua pergunta: "${message}"`; // Apenas o texto aqui

    // Cria o span para o emoji do robô

    // Adiciona o emoji e o texto ao wrapper do bot (ordem inversa para ficar à esquerda)
    botMessageWrapper.appendChild(botEmoji);
    botMessageWrapper.appendChild(botMessageText);
    chat.appendChild(botMessageWrapper);

    chat.scrollTop = chat.scrollHeight;
  }, 600);
}

// Permite enviar apertando "Enter"
input.addEventListener("keydown", (e) => {
  if (e.key === "Enter") {
    sendMessage();
  }
});
