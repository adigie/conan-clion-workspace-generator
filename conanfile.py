import os
import xml.etree.cElementTree as ET
from conans import ConanFile, tools


class ClionWorkspaceGenerator():
    def __init__(self, conanfile):
        self._build_type = str(conanfile.settings.build_type)
        self._generation_dir = conanfile.build_folder
        self._toolchain_file = tools.get_env("CONAN_CMAKE_TOOLCHAIN_FILE")
        self._workspace_path = os.path.join(conanfile.source_folder, ".idea")

    def _insert_configuration_element(self, node):
        configuration = ET.SubElement(node, "configuration")
        configuration.set("PROFILE_NAME", self._build_type)
        configuration.set("CONFIG_NAME", self._build_type)
        configuration.set("BUILD_OPTIONS", "-j {}".format(tools.cpu_count()))
        configuration.set("GENERATION_DIR", self._generation_dir)
        if self._toolchain_file:
            configuration.set(
                "GENERATION_OPTIONS", "-DCMAKE_TOOLCHAIN_FILE={}".format(self._toolchain_file))

    def _update_workspace_file(self, file_path):
        tree = ET.parse(file_path)
        project = tree.getroot()

        for component in project.findall("component"):
            if component.attrib["name"] == "CMakeSettings":
                for configurations in component.findall("configurations"):
                    configurations.clear()
                    self._insert_configuration_element(configurations)

        tree.write(file_path, encoding="UTF-8", xml_declaration=True)

    def _generate_workspace_file(self, file_path):
        project = ET.Element("project")
        project.set("version", "4")

        component = ET.SubElement(project, "component")
        component.set("name", "CMakeSettings")

        configurations = ET.SubElement(component, "configurations")
        self._insert_configuration_element(configurations)

        tree = ET.ElementTree(project)
        tree.write(file_path, encoding="UTF-8", xml_declaration=True)

    def generate(self):
        if not os.path.exists(self._workspace_path):
            os.makedirs(self._workspace_path)
        workspace_file_path = os.path.join(
            self._workspace_path, "workspace.xml")
        if os.path.exists(workspace_file_path):
            self._update_workspace_file(workspace_file_path)
        else:
            self._generate_workspace_file(workspace_file_path)


class Conan(ConanFile):
    pass
