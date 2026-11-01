import { useState } from "react";
import { hospital, departments } from "../data.js";

export default function Hero() {
  const [sent, setSent] = useState(false);   // has the form been sent?

  function handleSubmit(event) {
    event.preventDefault();   // stop the page from reloading
    setSent(true);            // for now we only show a thank-you message
  }

  return (
    <section className="hero-banner">
      <div className="wrap">
        <div className="breadcrumb">Home / Our Hospital</div>

        <div className="hero-grid">
          <div>
            <h1>{hospital.tagline}</h1>
            <p>{hospital.hours}</p>
            <a className="button" href="#appointment">Book an appointment</a>
          </div>

          <form className="enquiry" id="appointment" onSubmit={handleSubmit}>
            <h2>Enquiry Form</h2>
            {sent ? (
              <p className="thanks">Thank you! Our team will call you soon.</p>
            ) : (
              <>
                <input type="text" placeholder="Your name" required />
                <input type="tel" placeholder="Phone number" required />
                <select defaultValue="">
                  <option value="" disabled>Select department</option>
                  {departments.map((d) => (
                    <option key={d.name}>{d.name}</option>
                  ))}
                </select>
                <textarea
                  rows="3"
                  placeholder="Your message (please do not write medical details)"
                />
                <button type="submit">Send enquiry</button>
              </>
            )}
          </form>
        </div>
      </div>
    </section>
  );
}