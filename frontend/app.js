const analyzeButton = document.getElementById('analyze');
const queryInput = document.getElementById('query');
const status = document.getElementById('status');
const resultsSection = document.getElementById('results');
const keywordsList = document.getElementById('keywords');
const topicsContainer = document.getElementById('topics');
const trendsPre = document.getElementById('trends');
const painPointsList = document.getElementById('pain-points');
const rawPre = document.getElementById('raw');

const API_URL = 'http://localhost:8000/analyze';

function setStatus(message, isError = false) {
  status.textContent = message;
  status.classList.toggle('error', isError);
}

function renderKeywords(keywords) {
  keywordsList.innerHTML = '';
  keywords.forEach((keyword) => {
    const li = document.createElement('li');
    li.textContent = keyword;
    keywordsList.appendChild(li);
  });
}

function renderTopics(topics) {
  topicsContainer.innerHTML = '';
  topics.forEach((topic) => {
    const wrapper = document.createElement('div');
    wrapper.className = 'topic';
    const title = document.createElement('h3');
    title.textContent = `Topic ${topic.topic_id + 1}`;
    const terms = document.createElement('p');
    terms.textContent = topic.terms.join(', ');
    wrapper.appendChild(title);
    wrapper.appendChild(terms);
    topicsContainer.appendChild(wrapper);
  });
}

function renderPainPoints(painPoints) {
  painPointsList.innerHTML = '';
  painPoints.forEach((item) => {
    const li = document.createElement('li');
    li.innerHTML = `<strong>${item.title}</strong> <span>${item.view_count} views</span>`;
    painPointsList.appendChild(li);
  });
}

async function analyzeQuery() {
  const query = queryInput.value.trim();
  if (!query) {
    setStatus('Please enter a query.', true);
    return;
  }

  setStatus('Analyzing Stack Overflow data...');
  resultsSection.hidden = true;

  try {
    const response = await fetch(`${API_URL}?query=${encodeURIComponent(query)}`);
    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(errorText || 'Request failed.');
    }
    const data = await response.json();

    renderKeywords(data.top_keywords || []);
    renderTopics(data.topics || []);
    trendsPre.textContent = JSON.stringify(data.trends || [], null, 2);
    renderPainPoints(data.pain_points || []);
    rawPre.textContent = JSON.stringify(data, null, 2);
    resultsSection.hidden = false;
    setStatus('Analysis complete.');
  } catch (error) {
    setStatus(`Error: ${error.message}`, true);
  }
}

analyzeButton.addEventListener('click', analyzeQuery);
queryInput.addEventListener('keydown', (event) => {
  if (event.key === 'Enter') {
    analyzeQuery();
  }
});
