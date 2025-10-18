import json
from typing import Any
from xml.etree import ElementTree as ET


def create_junit_xml(safety_json: dict[str, Any]) -> ET.ElementTree:
    testsuite = ET.Element("testsuite")
    testsuite.set("name", "Safety Scan")

    vulns = 0
    for project in safety_json["scan_results"]["projects"]:
        for file in project["files"]:
            for dep in file["results"]["dependencies"]:
                for spec in dep["specifications"]:
                    if (
                        "vulnerabilities" in spec
                        and spec["vulnerabilities"]["known_vulnerabilities"]
                    ):
                        for vuln in spec["vulnerabilities"]["known_vulnerabilities"]:
                            vulns += 1
                            testcase = ET.SubElement(testsuite, "testcase")

                            current_version = (
                                spec["raw"].split("==")[1] if "==" in spec["raw"] else "unknown"
                            )
                            recommended = spec["vulnerabilities"]["remediation"]["recommended"]
                            test_name = (
                                f"{dep['name']}_{current_version}_"
                                + f"needs_upgrade_to_{recommended}_vuln_{vuln['id']}"
                            )

                            testcase.set("name", test_name)
                            testcase.set("classname", dep["name"])

                            failure = ET.SubElement(testcase, "failure")
                            remed = spec["vulnerabilities"]["remediation"]
                            message = f"Vulnerability in {dep['name']} {spec['raw']}\n"
                            message += f"Recommended version: {remed['recommended']}"
                            failure.set("message", message)
                            failure.text = message

    testsuite.set("tests", str(vulns))
    testsuite.set("failures", str(vulns))

    return ET.ElementTree(testsuite)


if __name__ == "__main__":
    with open("safety-report.json") as f:
        safety_json = json.load(f)

    junit = create_junit_xml(safety_json)
    junit.write("safety-report.xml", encoding="unicode", xml_declaration=True)
