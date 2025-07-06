(() => {
  const log = console.log; // Save original function
  log("Content js is loading");
  const searchEngineDomains = [
"google.com", "bing.com", "yahoo.com", "duckduckgo.com", "search.brave.com"
];
const currentDomain = window.location.hostname;
if (searchEngineDomains.some(domain => currentDomain.includes(domain))) {
console.log("Fake Ad Detector skipped: search engine domain.");
return;
}
const suspiciousKeywords = [
    "miracle cure",
    "lose weight fast",
    "burn fat instantly",
    "cure in 7 days",
    "natural cancer remedy",
    "drop 10 kg",
    "instant results",
    "100% effective",
    "clinically proven miracle",
    "secret health formula",
    "boost metabolism overnight",
    "fat burner",
    "no exercise needed",
    "eat anything and lose weight",
    "detox cleanse",
    "lose belly fat without effort",
    "belly fat solution",
    "reverse diabetes naturally",

    "look 10 years younger",
    "anti-aging breakthrough",
    "instant fairness",
    "remove wrinkles overnight",
    "skin whitening in 3 days",
    "blemish-free in 24 hours",
    "doctors hate this cream",
    "age-reversing formula",
    "flawless skin overnight",

    "make money fast",
    "double your income overnight",
    "earn ₹5000/hour",
    "guaranteed investment return",
    "passive income system",
    "get rich quick",
    "make money online",
    "work from home and become a millionaire",
    "unlimited earning potential",
    "zero-risk investment",

    "crack exam in 10 days",
    "100% job guarantee",
    "instant certificate",
    "shortcut to success",
    "get a certificate instantly",
    "learn AI in 2 hours",
    "become expert in 1 day",
    "no experience needed",

   
    "limited time offer",
    "exclusive deal",
    "act now",
    "hidden trick",
    "never seen before",
    "you won’t believe this",
    "what happened next shocked me",
    "doctors hate this trick",
    "shocking truth",
    "this is not a scam",
    "only 3 spots left",
    "shocking secret doctors hide from you",
    "one simple trick",
    "they don't want you to know",
    "what happens next will shock you",
    "click to find out",
    "secret revealed",
    "too good to be true"

];

 const elements = document.querySelectorAll("p, div, span");

  elements.forEach(el => {
    const text = el.innerText?.toLowerCase();
    if (!text || text.length < 15 || el.hasAttribute("data-fake-ad-checked")) return;

    suspiciousKeywords.forEach(keyword => {
      if (text.includes(keyword)) {
        el.setAttribute("data-fake-ad-checked", "true"); // Prevent repeated checks
        el.style.border = "2px solid orange";
        el.setAttribute("title", "Analyzing ad...");

        fetch("http://localhost:5000/analyze", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ text: el.innerText })
        })
        .then(res => res.json())
        .then(data => {
          const verdict = data.verdict || "Unknown";
          const trust = data.trust_score !== undefined ? `${data.trust_score}/100` : "N/A";
          let color = "gray";

          if (verdict === "Safe") color = "green";
          else if (verdict === "Exaggerated") color = "orange";
          else if (verdict === "Misleading") color = "red";

          el.style.border = `2px solid ${color}`;
          el.setAttribute("title", `Verdict: ${verdict} |  Trust Score: ${trust}`); 
          console.log(` Verdict for element: ${verdict}, Trust: ${trust}`);

        })
        .catch(err => {
          el.style.border = "2px dashed gray";
          el.setAttribute("title", "Error contacting server");
          console.error(err);
        });
      }
    });
  });
})();