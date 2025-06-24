const chat = document.querySelector(".chat");
const input = document.getElementById("messageInput");

async function sendMessage() {
  const message = input.value.trim();
  if (message === "") return;

  // Mensagem do usuário
  const userMessageWrapper = document.createElement("div");
  userMessageWrapper.classList.add("message-wrapper", "user-wrapper");
  const userMessageText = document.createElement("div");
  userMessageText.classList.add("message", "user");
  userMessageText.textContent = message;
  const userEmoji = document.createElement("span");
  userEmoji.classList.add("message-emoji");
  userEmoji.textContent = "🧑‍🏫";
  userMessageWrapper.appendChild(userMessageText);
  userMessageWrapper.appendChild(userEmoji);
  chat.appendChild(userMessageWrapper);

  input.value = "";
  chat.scrollTop = chat.scrollHeight;
  // Enviar para API
  try {
    const response = await fetch("http://localhost:8000/query/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        ask: message,
        top_k: 5,
        temperature: 0.5,
      }),
    });

    if (!response.ok) {
      throw new Error(`Erro na API: ${response.statusText}`);
    }

    const data = await response.json();

    // Mensagem do bot com a resposta da API
    const botMessageWrapper = document.createElement("div");
    botMessageWrapper.classList.add("message-wrapper", "bot-wrapper");
    const botEmoji = document.createElement("span");
    botEmoji.textContent = "🤖";
    botEmoji.classList.add("message-emoji");
    const botMessageText = document.createElement("div");
    botMessageText.classList.add("message", "bot");
    botMessageText.textContent = data.response || "Não recebi resposta da API.";
    botMessageWrapper.appendChild(botEmoji);
    botMessageWrapper.appendChild(botMessageText);
    chat.appendChild(botMessageWrapper);

    chat.scrollTop = chat.scrollHeight;
  } catch (error) {
    console.error(error);
    // Mostra erro no chat
    const botMessageWrapper = document.createElement("div");
    botMessageWrapper.classList.add("message-wrapper", "bot-wrapper");
    const botEmoji = document.createElement("span");
    botEmoji.textContent = "⚠️";
    botEmoji.classList.add("message-emoji");
    const botMessageText = document.createElement("div");
    botMessageText.classList.add("message", "bot");
    botMessageText.textContent = "Erro ao consultar a API.";
    botMessageWrapper.appendChild(botEmoji);
    botMessageWrapper.appendChild(botMessageText);
    chat.appendChild(botMessageWrapper);
    chat.scrollTop = chat.scrollHeight;
  }

  // Permite enviar apertando "Enter"
  input.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      sendMessage();
    }
  });
}
