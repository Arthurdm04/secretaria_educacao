// Em static/js/dashboard.js

// O código só roda depois que o HTML da página estiver completamente carregado.
document.addEventListener("DOMContentLoaded", () => {
  // ----------------------------------------------------------------
  // PASSO 1: VERIFICAÇÃO INICIAL E SELEÇÃO DE ELEMENTOS
  // ----------------------------------------------------------------

  // Protege a página: se não houver token, o AuthManager redireciona para o login.
  AuthManager.protectPage();

  // Seleciona todos os elementos da página que vamos manipular.
  // Fazer isso no início deixa o código mais organizado.
  const userInfoP = document.getElementById("user-info");
  const logoutButton = document.getElementById("logout-button");

  // Coluna da Esquerda (Instituições)
  const institutionListContainer = document.getElementById(
    "institution-list-container"
  );
  const addSchoolBtn = document.getElementById("add-school-btn");

  // Coluna da Direita (Turmas)
  const classListContainer = document.getElementById("class-list-container");
  const addClassBtn = document.getElementById("add-class-btn");

  // Elementos do Modal de Escola
  const schoolModal = document.getElementById("school-modal-overlay");
  const closeSchoolModalBtn = document.getElementById("close-school-modal");
  const schoolForm = document.getElementById("form-escola");
  const schoolMessageArea = document.getElementById("escola-message-area");

  // Elementos do Modal de Turma
  const classModal = document.getElementById("class-modal-overlay");
  const closeClassModalBtn = document.getElementById("close-class-modal");
  const classForm = document.getElementById("form-turma");
  const classMessageArea = document.getElementById("turma-message-area");
  const schoolSelectInClassForm = document.getElementById("school-select");

  // Variável para guardar os dados carregados da API
  let schoolsData = [];
  let classesData = [];

  // ----------------------------------------------------------------
  // PASSO 2: FUNÇÕES PARA BUSCAR DADOS DA API E RENDERIZAR
  // ----------------------------------------------------------------

  // Busca as escolas e as exibe na coluna da esquerda.
  async function loadSchools() {
    institutionListContainer.innerHTML = "<p>Carregando instituições...</p>";
    try {
      const response = await AuthManager.fetchWithAuth(
        "http://127.0.0.1:8000/schools/"
      );
      schoolsData = await response.json(); // Armazena os dados globalmente neste script

      if (schoolsData.length === 0) {
        institutionListContainer.innerHTML =
          "<p>Nenhuma instituição cadastrada.</p>";
      } else {
        const schoolItemsHtml = schoolsData
          .map(
            (school) => `
                    <div class="institution-item" data-school-id="${school.id}">
                        ${school.name}
                    </div>
                `
          )
          .join("");
        institutionListContainer.innerHTML = schoolItemsHtml;
      }
      populateSchoolsDropdown(); // Atualiza o dropdown no formulário de turma
    } catch (error) {
      console.error("Erro ao carregar escolas:", error);
      institutionListContainer.innerHTML =
        '<p class="text-red-500">Erro ao carregar instituições.</p>';
    }
  }

  // Busca as turmas e as exibe na coluna da direita.
  async function loadClasses() {
    classListContainer.innerHTML = "<p>Carregando turmas...</p>";
    try {
      const response = await AuthManager.fetchWithAuth(
        "http://127.0.0.1:8000/classes/show"
      );
      classesData = await response.json();

      if (classesData.length === 0) {
        classListContainer.innerHTML =
          "<p>Nenhuma turma cadastrada para esta escola.</p>";
      } else {
        const classCardsHtml = classesData
          .map(
            (turma) => `
                    <div class="bg-white p-4 rounded-lg shadow-md flex justify-between items-center mb-3">
                        <div>
                            <h4 class="font-bold text-lg text-gray-800">${turma.name}</h4>
                            <p class="text-sm text-gray-500">Ano: ${turma.year}</p>
                        </div>
                        <button class="acessar-turma-btn bg-blue-500 text-white px-3 py-1 rounded-md hover:bg-blue-600">Acessar</button>
                    </div>
                `
          )
          .join("");
        classListContainer.innerHTML = classCardsHtml;
      }
    } catch (error) {
      console.error("Erro ao carregar turmas:", error);
      classListContainer.innerHTML =
        '<p class="text-red-500">Erro ao carregar turmas.</p>';
    }
  }

  // Popula o dropdown de escolas no formulário de criação de turma.
  function populateSchoolsDropdown() {
    schoolSelectInClassForm.innerHTML =
      '<option value="">Selecione uma escola</option>';
    if (schoolsData.length > 0) {
      schoolsData.forEach((school) => {
        const option = document.createElement("option");
        option.value = school.id;
        option.textContent = school.name;
        schoolSelectInClassForm.appendChild(option);
      });
    }
  }

  // ----------------------------------------------------------------
  // PASSO 3: LÓGICA DE EVENTOS (CLICKS E SUBMISSÕES)
  // ----------------------------------------------------------------

  // --- Controle dos Modais ---
  addSchoolBtn.addEventListener("click", () =>
    schoolModal.classList.remove("hidden")
  );
  closeSchoolModalBtn.addEventListener("click", () =>
    schoolModal.classList.add("hidden")
  );
  schoolModal.addEventListener("click", (e) => {
    if (e.target === schoolModal) schoolModal.classList.add("hidden");
  });

  addClassBtn.addEventListener("click", () =>
    classModal.classList.remove("hidden")
  );
  closeClassModalBtn.addEventListener("click", () =>
    classModal.classList.add("hidden")
  );
  classModal.addEventListener("click", (e) => {
    if (e.target === classModal) classModal.classList.add("hidden");
  });

  // --- Submissão do Formulário de Escola ---
  schoolForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    schoolMessageArea.innerText = "";
    const schoolName = document.getElementById("nome-escola").value;
    const schoolAddress = document.getElementById("endereco-escola").value;

    try {
      const response = await AuthManager.fetchWithAuth(
        "http://127.0.0.1:8000/schools/",
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ name: schoolName, address: schoolAddress }),
        }
      );

      if (response.ok) {
        alert("Instituição cadastrada com sucesso!");
        schoolModal.classList.add("hidden");
        schoolForm.reset();
        loadSchools(); // Atualiza a lista de escolas na tela!
      } else {
        const errorData = await response.json();
        schoolMessageArea.innerText = errorData.detail || "Erro ao cadastrar.";
      }
    } catch (error) {
      schoolMessageArea.innerText = "Erro de conexão.";
      console.error("Erro ao cadastrar escola:", error);
    }
  });

  // --- Submissão do Formulário de Turma ---
  classForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    classMessageArea.innerText = "";

    const classData = {
      name: document.getElementById("nome-turma").value,
      year: parseInt(document.getElementById("ano-letivo").value),
      school_id: parseInt(document.getElementById("school-select").value),
    };

    if (!classData.school_id) {
      classMessageArea.innerText = "Por favor, selecione uma escola.";
      return;
    }

    try {
      const response = await AuthManager.fetchWithAuth(
        "http://127.0.0.1:8000/classes/",
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(classData),
        }
      );

      if (response.ok) {
        alert("Turma cadastrada com sucesso!");
        classModal.classList.add("hidden");
        classForm.reset();
        loadClasses(); // Atualiza a lista de turmas na tela!
      } else {
        const errorData = await response.json();
        classMessageArea.innerText =
          errorData.detail || "Não foi possível cadastrar a turma.";
      }
    } catch (error) {
      console.error("Erro ao cadastrar turma:", error);
      classMessageArea.innerText = error.message;
    }
  });

  // --- Botão de Logout ---
  logoutButton.addEventListener("click", () => AuthManager.logout());

  // ----------------------------------------------------------------
  // PASSO 4: INICIALIZAÇÃO DA PÁGINA
  // ----------------------------------------------------------------

  // Busca os dados do usuário. Se tiver sucesso, carrega o resto dos dados da página.
  AuthManager.fetchWithAuth("http://127.0.0.1:8000/users/me")
    .then((response) => response.json())
    .then((userData) => {
      userInfoP.innerHTML = `Olá, <strong>${userData.full_name}</strong>!`;
      // Agora que sabemos que o usuário está logado, carregamos os dados principais.
      loadSchools();
      // A função loadClasses() pode ser chamada aqui ou quando uma escola for selecionada.
      // Por enquanto, vamos deixar o container de turmas com a mensagem inicial.
    })
    .catch((error) => {
      console.error("Falha na autenticação inicial:", error);
      // O AuthManager.protectPage() e o fetchWithAuth já cuidam do redirecionamento.
    });
});
