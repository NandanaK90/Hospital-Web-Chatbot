import { hospital, departments, doctors } from "./data.js";
import Header from "./components/Header.jsx";
import Hero from "./components/Hero.jsx";
import ChatWidget from "./components/ChatWidget.jsx";

export default function App() {
  return (
    <>
      <Header />
      <Hero />

      <section id="departments" className="wrap section">
        <h2>Our departments</h2>
        <div className="grid">
          {departments.map((d) => (
            <div className="card" key={d.name}>
              <h3>{d.name}</h3>
              <p>{d.text}</p>
            </div>
          ))}
        </div>
      </section>

      <section id="doctors" className="wrap section">
        <h2>Our doctors</h2>
        {departments.map((d) => (
          <div key={d.name}>
            <h3 className="dept-title">{d.name}</h3>
            <div className="grid">
              {doctors
                .filter((doc) => doc.dept === d.name)
                .map((doc) => (
                  <div className="card" key={doc.name}>
                    <h3>{doc.name}</h3>
                    <p>{doc.days}</p>
                  </div>
                ))}
            </div>
          </div>
        ))}
      </section>

      <section id="contact" className="wrap section">
        <h2>Contact us</h2>
        <div className="card">
          <p>Phone: {hospital.phone}</p>
          <p>Emergency (24 hours): {hospital.emergencyPhone}</p>
          <p>Email: {hospital.email}</p>
          <p>Address: {hospital.address}</p>
        </div>
      </section>

      <footer className="footer">
        <div className="wrap">
          &copy; {new Date().getFullYear()} {hospital.name}. Sample website for learning.
        </div>
      </footer>

      <ChatWidget />
    </>
  );
}