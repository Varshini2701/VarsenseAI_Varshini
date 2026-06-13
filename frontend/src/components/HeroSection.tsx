import React from 'react';

export const HeroSection: React.FC = () => {
  const steps = [
    { title: "Calendar Data", icon: "📅", description: "Raw meeting calendars ingested." },
    { title: "AI Attribution", icon: "🧠", description: "Gemini auto-tags to projects." },
    { title: "Cost Calculation", icon: "💸", description: "HR burn-rate dynamically computed." },
    { title: "Project Insights", icon: "📈", description: "Executive-level dashboard." },
  ];

  return (
    <div className="hero-section">
      <div className="hero-content">
        <h1 className="hero-title">VarSense AI</h1>
        <p className="hero-subtitle">Transform Meetings into Cost Intelligence</p>
      </div>

      <div className="workflow-visualization">
        {steps.map((step, index) => (
          <React.Fragment key={step.title}>
            <div className="workflow-step">
              <div className="step-icon">{step.icon}</div>
              <h3 className="step-title">{step.title}</h3>
              <p className="step-description">{step.description}</p>
            </div>
            {index < steps.length - 1 && (
              <div className="workflow-arrow">
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M5 12h14M12 5l7 7-7 7"/>
                </svg>
              </div>
            )}
          </React.Fragment>
        ))}
      </div>
    </div>
  );
};
