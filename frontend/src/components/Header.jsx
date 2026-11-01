import {
  FaHospital,
  FaStethoscope,
  FaRegCalendarCheck,
  FaGlobeAsia,
  FaChevronDown,
  FaThLarge,
} from "react-icons/fa";
import { hospital, departments, branches, topLinks } from "../data.js";

export default function Header() {
  return (
    <header id="top">
      {/* Thin bar on top */}
      <div className="utility">
        <div className="wrap utility-inner">
          {topLinks.map((link) => (
            <a key={link} href="#contact">{link}</a>
          ))}
        </div>
      </div>

      {/* Main bar */}
      <div className="mainbar">
        <div className="wrap mainbar-inner">
          <a className="brand" href="#top">
            <span className="brand-name">{hospital.name}</span>
            <span className="brand-place">{hospital.place}</span>
          </a>

          <nav className="mainnav">
            <div className="nav-item">
              <a href="#contact">
                <FaHospital className="nav-icon" />
                <span>Our<br />Hospitals</span>
                <FaChevronDown className="caret" />
              </a>
              <ul className="dropdown">
                {branches.map((b) => (
                  <li key={b}><a href="#contact">{b}</a></li>
                ))}
              </ul>
            </div>

            <div className="nav-item">
              <a href="#departments">
                <FaStethoscope className="nav-icon" />
                <span>Our<br />Specialities</span>
                <FaChevronDown className="caret" />
              </a>
              <ul className="dropdown">
                {departments.map((d) => (
                  <li key={d.name}><a href="#departments">{d.name}</a></li>
                ))}
              </ul>
            </div>

            <div className="nav-item">
              <a href="#appointment">
                <FaRegCalendarCheck className="nav-icon" />
                <span>Book An<br />Appointment</span>
              </a>
            </div>

            <div className="nav-item">
              <a href="#contact">
                <FaGlobeAsia className="nav-icon" />
                <span>International<br />Patients</span>
              </a>
            </div>

            <div className="nav-item">
              <a href="#doctors" aria-label="Doctors">
                <FaThLarge className="nav-icon" />
              </a>
            </div>
          </nav>
        </div>
      </div>
    </header>
  );
}