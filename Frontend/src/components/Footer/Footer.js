
import React from "react";
import { Container } from "reactstrap";

import PropTypes from "prop-types";

function Footer(props) {
  return (
    <footer className={"footer" + (props.default ? " footer-default" : "")}>
      <Container fluid={props.fluid ? true : false}>
        <nav>
          <ul>
            <li>
              <a
                href="https://www.xloopdigital.com/"
                target="_blank"
              >
               Xloop
              </a>
            </li>
            <li>
              <a
                href= "https://www.xloopdigital.com/about-xloop.html"
                target="_blank"
              >
                About Us
              </a>
            </li>
            <li>
              <a
                href="https://www.xloopdigital.com/career.html"
                target="_blank"
              >
                Blog
              </a>
            </li>
          </ul>
        </nav>
        <div className="copyright">
          &copy; {1900 + new Date().getYear()}, Designed by{" "} & Coded by{" "}
          <a
            href="https://github.com/Muhammad-Danish-011"
            target="_blank"
            rel="noopener noreferrer"
          >
           Muhammad Danish
          </a>
        </div>
      </Container>
    </footer>
  );
}

Footer.propTypes = {
  default: PropTypes.bool,
  fluid: PropTypes.bool,
};

export default Footer;
