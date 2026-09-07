document.addEventListener("DOMContentLoaded", () => {
  // Tabs Navigation
  const tabBtns = document.querySelectorAll(".tab-btn");
  const tabContents = document.querySelectorAll(".tab-content");

  tabBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      const target = btn.getAttribute("data-tab");
      tabBtns.forEach(b => {
        b.classList.remove("active", "text-white");
        b.classList.add("text-slate-400");
      });
      tabContents.forEach(tc => tc.classList.add("hidden"));

      btn.classList.add("active", "text-white");
      btn.classList.remove("text-slate-400");
      document.getElementById(target).classList.remove("hidden");

      if (target === "contradictions-tab") loadContradictions();
      if (target === "unanswerable-tab") loadUnanswerables();
      if (target === "corpus-tab") loadCorpus();
    });
  });

  // Query Execution
  const queryInput = document.getElementById("query-input");
  const askBtn = document.getElementById("ask-btn");
  const modelSelect = document.getElementById("model-select");
  const loadingSpinner = document.getElementById("loading-spinner");
  const resultCard = document.getElementById("result-card");

  async function executeQuery(queryText) {
    if (!queryText.trim()) return;

    resultCard.classList.add("hidden");
    loadingSpinner.classList.remove("hidden");

    try {
      const resp = await fetch("/api/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          query: queryText,
          model: modelSelect.value
        })
      });

      const data = await resp.json();
      displayResult(data);
    } catch (err) {
      alert("Error querying regulations: " + err.message);
    } finally {
      loadingSpinner.classList.add("hidden");
    }
  }

  askBtn.addEventListener("click", () => {
    executeQuery(queryInput.value);
  });

  queryInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && (e.metaKey || e.ctrlKey)) {
      executeQuery(queryInput.value);
    }
  });

  // Sample Query Buttons
  document.querySelectorAll(".sample-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      const q = btn.getAttribute("data-query");
      queryInput.value = q;
      executeQuery(q);
    });
  });

  function displayResult(data) {
    resultCard.classList.remove("hidden");

    // Status Badge
    const statusBadge = document.getElementById("status-badge");
    statusBadge.textContent = data.status_label;
    statusBadge.className = "px-3 py-1 rounded-full text-xs font-extrabold tracking-wide uppercase ";
    
    if (data.status === "CONTRADICTION") {
      statusBadge.classList.add("badge-contradiction");
    } else if (data.status === "UNANSWERABLE") {
      statusBadge.classList.add("badge-unanswerable");
    } else {
      statusBadge.classList.add("badge-answered");
    }

    document.getElementById("model-badge").textContent = `Engine: ${data.model_used}`;
    document.getElementById("latency-text").textContent = `${data.latency_ms}ms`;

    // Contradiction Details
    const contraBanner = document.getElementById("contradiction-banner");
    const confGrid = document.getElementById("conflicting-clauses-container");
    const confList = document.getElementById("conflicting-clauses-grid");

    if (data.contradiction && data.contradiction.detected) {
      contraBanner.classList.remove("hidden");
      confGrid.classList.remove("hidden");
      document.getElementById("contradiction-topic").textContent = `Contradiction: ${data.contradiction.title}`;
      document.getElementById("contradiction-tension").textContent = data.contradiction.point_of_tension;
      document.getElementById("contradiction-ambiguity").textContent = data.contradiction.administrative_ambiguity;

      confList.innerHTML = "";
      data.contradiction.conflicting_clauses.forEach((c, idx) => {
        const card = document.createElement("div");
        card.className = "bg-slate-950/90 border border-amber-500/40 rounded-xl p-3.5 text-xs space-y-2";
        card.innerHTML = `
          <div class="flex items-center justify-between font-mono text-[11px] text-amber-400">
            <span class="font-bold">${c.clause_ref}</span>
            <span class="text-slate-400 truncate max-w-[120px]">${c.document}</span>
          </div>
          <div class="font-semibold text-slate-200">${c.clause_title}</div>
          <p class="text-slate-300 italic bg-amber-950/20 p-2 rounded border-l-2 border-amber-500 text-[11.5px]">"${c.snippet}"</p>
        `;
        confList.appendChild(card);
      });
    } else {
      contraBanner.classList.add("hidden");
      confGrid.classList.add("hidden");
    }

    // Answer Text
    document.getElementById("answer-text").innerHTML = formatMarkdown(data.answer);

    // Citations
    const citContainer = document.getElementById("citations-container");
    const citList = document.getElementById("citations-list");
    citList.innerHTML = "";

    if (data.citations && data.citations.length > 0) {
      citContainer.classList.remove("hidden");
      data.citations.forEach(c => {
        const item = document.createElement("div");
        item.className = "bg-slate-950/60 border border-slate-800 rounded-lg p-3 text-xs flex flex-col gap-1";
        item.innerHTML = `
          <div class="flex items-center justify-between font-mono">
            <span class="text-indigo-400 font-bold">${c.clause_ref}: ${c.clause_title}</span>
            <span class="text-slate-400">${c.document}</span>
          </div>
          <p class="text-slate-300 text-[11.5px]">${c.snippet}</p>
        `;
        citList.appendChild(item);
      });
    } else {
      citContainer.classList.add("hidden");
    }

    resultCard.scrollIntoView({ behavior: "smooth", block: "nearest" });
  }

  function formatMarkdown(text) {
    if (!text) return "";
    let html = text
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.*?)\*/g, '<em>$1</em>')
      .replace(/^>\s*(.*?)$/gm, '<blockquote class="border-l-2 border-slate-600 pl-3 italic my-2 text-slate-300">$1</blockquote>')
      .replace(/\n\n/g, '<br><br>');
    return html;
  }

  // Load Planted Contradictions
  let contradictionsLoaded = false;
  async function loadContradictions() {
    if (contradictionsLoaded) return;
    try {
      const resp = await fetch("/api/contradictions");
      const list = await resp.json();
      const container = document.getElementById("planted-contradictions-list");
      container.innerHTML = "";

      list.forEach(c => {
        const card = document.createElement("div");
        card.className = "bg-slate-950 border border-slate-800 rounded-xl p-5 space-y-4";
        
        let clausesHtml = "";
        c.clauses.forEach(cl => {
          clausesHtml += `
            <div class="bg-slate-900/90 border border-slate-800 p-3 rounded-lg text-xs">
              <div class="text-indigo-400 font-mono font-bold">${cl.clause_ref}: ${cl.clause_title} (${cl.document})</div>
              <p class="text-slate-300 mt-1 italic">"${cl.text}"</p>
            </div>
          `;
        });

        card.innerHTML = `
          <div class="flex items-center justify-between">
            <h3 class="text-sm font-bold text-amber-400 font-mono">[${c.cid}] ${c.title}</h3>
            <span class="text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded bg-amber-500/20 text-amber-300 border border-amber-500/30">
              ${c.topic}
            </span>
          </div>
          <p class="text-xs text-slate-300">${c.description}</p>
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">${clausesHtml}</div>
          <div class="bg-amber-950/30 border-l-2 border-amber-500 p-3 text-xs text-amber-200">
            <strong>Point of Tension:</strong> ${c.point_of_tension}
          </div>
          <div class="flex items-center gap-2 pt-2">
            <span class="text-xs text-slate-400 font-semibold">Test Trigger:</span>
            <button class="test-trigger-btn text-xs font-mono bg-indigo-950/60 hover:bg-indigo-900/60 text-indigo-300 border border-indigo-800/60 px-2.5 py-1 rounded transition" data-q="${c.test_queries[0]}">
              "${c.test_queries[0]}" ↗
            </button>
          </div>
        `;
        container.appendChild(card);
      });

      container.querySelectorAll(".test-trigger-btn").forEach(btn => {
        btn.addEventListener("click", () => {
          const q = btn.getAttribute("data-q");
          document.querySelector('.tab-btn[data-tab="qa-tab"]').click();
          queryInput.value = q;
          executeQuery(q);
        });
      });

      contradictionsLoaded = true;
    } catch (e) {
      console.error(e);
    }
  }

  // Load Unanswerable Questions
  let unanswerablesLoaded = false;
  async function loadUnanswerables() {
    if (unanswerablesLoaded) return;
    try {
      const resp = await fetch("/api/unanswerable-testset");
      const list = await resp.json();
      const container = document.getElementById("unanswerables-list");
      container.innerHTML = "";

      list.forEach(u => {
        const card = document.createElement("div");
        card.className = "bg-slate-950 border border-slate-800 rounded-xl p-4 text-xs space-y-3 flex flex-col justify-between";
        card.innerHTML = `
          <div>
            <div class="flex items-center justify-between font-mono text-[10px] text-purple-400 mb-1">
              <span>[${u.uid}]</span>
              <span class="px-2 py-0.5 rounded bg-purple-950/60 text-purple-300 border border-purple-800/60">${u.category}</span>
            </div>
            <div class="font-bold text-slate-200 text-sm mb-2">"${u.question}"</div>
            <p class="text-slate-400 text-[11.5px] mb-2"><strong class="text-slate-300">Why Unanswerable:</strong> ${u.why_unanswerable}</p>
            <div class="text-[10.5px] text-slate-500 font-mono">
              Adjacent: ${u.adjacent_clauses.join(", ")}
            </div>
          </div>
          <div class="pt-2 border-t border-slate-800/80">
            <button class="test-unans-btn text-[11px] text-indigo-400 hover:text-indigo-300 font-semibold flex items-center gap-1" data-q="${u.question}">
              Test Refusal in Advisor ↗
            </button>
          </div>
        `;
        container.appendChild(card);
      });

      container.querySelectorAll(".test-unans-btn").forEach(btn => {
        btn.addEventListener("click", () => {
          const q = btn.getAttribute("data-q");
          document.querySelector('.tab-btn[data-tab="qa-tab"]').click();
          queryInput.value = q;
          executeQuery(q);
        });
      });

      unanswerablesLoaded = true;
    } catch (e) {
      console.error(e);
    }
  }

  // Load Corpus Explorer
  let corpusLoaded = false;
  async function loadCorpus() {
    if (corpusLoaded) return;
    try {
      const resp = await fetch("/api/corpus");
      const data = await resp.json();

      document.getElementById("corpus-word-count").textContent = `${data.total_words.toLocaleString()} words loaded`;
      const grid = document.getElementById("corpus-docs-grid");
      grid.innerHTML = "";

      data.documents.forEach(doc => {
        const card = document.createElement("div");
        card.className = "clause-card bg-slate-950 border border-slate-800 rounded-xl p-4 text-xs space-y-2 cursor-pointer";
        card.innerHTML = `
          <div class="flex items-center justify-between font-mono text-[10px] text-slate-400">
            <span class="uppercase px-1.5 py-0.5 rounded bg-slate-800 text-slate-300">${doc.file_type}</span>
            <span>${doc.word_count.toLocaleString()} words</span>
          </div>
          <h4 class="font-bold text-slate-100 text-sm">${doc.title}</h4>
          <p class="font-mono text-[11px] text-slate-400">${doc.filename}</p>
          <div class="flex items-center justify-between pt-2 border-t border-slate-800 text-[11px] text-indigo-400">
            <span>${doc.clause_count} clauses parsed</span>
            <span>View Clauses →</span>
          </div>
        `;
        card.addEventListener("click", () => openDocViewer(doc.id, doc.title));
        grid.appendChild(card);
      });

      corpusLoaded = true;
    } catch (e) {
      console.error(e);
    }
  }

  async function openDocViewer(docId, title) {
    const viewer = document.getElementById("doc-viewer");
    const viewerTitle = document.getElementById("viewer-title");
    const viewerClauses = document.getElementById("viewer-clauses");

    viewerTitle.textContent = title;
    viewerClauses.innerHTML = "<div class='text-xs text-slate-500 font-mono'>Loading clauses...</div>";
    viewer.classList.remove("hidden");

    try {
      const resp = await fetch(`/api/corpus/document/${docId}`);
      const data = await resp.json();
      viewerClauses.innerHTML = "";

      data.clauses.forEach(c => {
        const el = document.createElement("div");
        el.className = "bg-slate-900 border border-slate-800 p-3 rounded-lg text-xs space-y-1";
        el.innerHTML = `
          <div class="flex items-center justify-between font-mono text-[11px] text-indigo-400">
            <span class="font-bold">${c.clause_id}: ${c.title}</span>
            <span class="text-slate-500">${c.word_count} words</span>
          </div>
          <div class="text-[10px] text-slate-500">${c.section_id}</div>
          <p class="text-slate-300 whitespace-pre-wrap mt-1">${c.content}</p>
        `;
        viewerClauses.appendChild(el);
      });
      viewer.scrollIntoView({ behavior: "smooth" });
    } catch (e) {
      console.error(e);
    }
  }

  document.getElementById("close-viewer").addEventListener("click", () => {
    document.getElementById("doc-viewer").classList.add("hidden");
  });

  // Automated Benchmark Runner
  const runBenchBtn = document.getElementById("run-bench-btn");
  runBenchBtn.addEventListener("click", async () => {
    runBenchBtn.disabled = true;
    runBenchBtn.innerHTML = `
      <div class="animate-spin rounded-full h-3.5 w-3.5 border-t-2 border-b-2 border-white"></div>
      <span>Running 40-Test Suite...</span>
    `;

    try {
      const resp = await fetch("/api/benchmark/run", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ model: modelSelect.value })
      });
      const res = await resp.json();

      document.getElementById("metric-overall").textContent = `${res.overall_accuracy}%`;
      document.getElementById("metric-unans").textContent = `${res.unanswerable_accuracy}%`;
      document.getElementById("metric-contra").textContent = `${res.contradiction_accuracy}%`;
      document.getElementById("metric-ans").textContent = `${res.answerable_accuracy}%`;

      const tbody = document.getElementById("bench-log-rows");
      tbody.innerHTML = "";

      res.details.forEach(item => {
        const tr = document.createElement("tr");
        tr.className = item.passed ? "hover:bg-slate-900/60" : "bg-red-950/20 hover:bg-red-950/30";
        
        const badgeColor = item.passed 
          ? "bg-emerald-950/80 text-emerald-300 border-emerald-800/80" 
          : "bg-red-950/80 text-red-300 border-red-800/80";

        tr.innerHTML = `
          <td class="p-3 font-mono text-[10px] text-slate-400">${item.test_type}</td>
          <td class="p-3 font-mono font-bold text-slate-300">${item.id}</td>
          <td class="p-3 text-slate-200 max-w-xs truncate">${item.query}</td>
          <td class="p-3 font-mono text-[10.5px] text-slate-400">${item.expected_status}</td>
          <td class="p-3 font-mono text-[10.5px] ${item.actual_status === item.expected_status ? 'text-emerald-400' : 'text-red-400'}">${item.actual_status}</td>
          <td class="p-3">
            <span class="px-2 py-0.5 rounded text-[10px] font-bold border ${badgeColor}">
              ${item.passed ? "PASSED" : "FAILED"}
            </span>
          </td>
          <td class="p-3 font-mono text-slate-400">${item.latency_ms}ms</td>
        `;
        tbody.appendChild(tr);
      });
    } catch (e) {
      alert("Benchmark failed: " + e.message);
    } finally {
      runBenchBtn.disabled = false;
      runBenchBtn.innerHTML = `
        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <span>Run Full 40-Test Suite</span>
      `;
    }
  });

  // Initial Load of Corpus Stats
  fetch("/api/corpus").then(r => r.json()).then(d => {
    document.getElementById("corpus-word-count").textContent = `${d.total_words.toLocaleString()} words loaded`;
  }).catch(() => {});
});
