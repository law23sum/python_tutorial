import React from "react";

const LoadError = function() {
  return (
    <section className="app-card">
      <h2 className="pg-subtitle">Sorry, there was an error loading your data.</h2>
      <div className="pg-content">
        <p>
          Check your internet connection and try reloading the page.
        </p>
        <p>
          If you are the site administrator and setting up your site for the first time, see the documentation to resolve this:
          <a href="https://docs.saaspegasus.com/apis/#api-client-requests-are-failing" target="_blank">
            Troubleshooting API errors.
          </a>
        </p>
      </div>
    </section>
  );
};

export default LoadError;
