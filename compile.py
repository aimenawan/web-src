from jinja2 import Environment
import os
import shutil
from jinja2 import BaseLoader, TemplateNotFound
from os.path import join, exists, getmtime


class Loader(BaseLoader):
    def __init__(self, path):
        self.path = path

    def get_source(self, environment, template):
        path = join(self.path, template)
        if not exists(path):
            raise TemplateNotFound(template)
        mtime = getmtime(path)
        with open(path, "r") as f:
            source = f.read()
        return source, path, lambda: mtime == getmtime(path)


class SourceBundle(object):
    def __init__(
        self, static_dir="static", src_dir="src", templates=None, dist_dir="docs"
    ):
        if templates is None:
            self.templates = ["index.html"]
        else:
            self.templates = templates
        self.static_dir = static_dir
        self.src_dir = src_dir
        self.dist_dir = dist_dir

    def _root(self):
        return os.path.dirname(os.path.abspath(__file__))

    def clean(self):
        if os.path.exists(self.dist_dir):
            shutil.rmtree(self.dist_dir)

    def build(self, **kwargs):
        if not os.path.exists(os.path.join(self._root(), self.dist_dir)):
            os.mkdir(os.path.join(self._root(), self.dist_dir))
        if self.static_dir is not None:
            if os.path.exists(
                os.path.join(self._root(), self.dist_dir, self.static_dir)
            ):
                shutil.rmtree(
                    os.path.join(self._root(), self.dist_dir, self.static_dir)
                )
            shutil.copytree(
                os.path.join(self._root(), self.src_dir, self.static_dir),
                os.path.join(self._root(), self.dist_dir, self.static_dir),
            )
        env = Environment(loader=Loader(os.path.join(self._root(), self.src_dir)))
        for template in self.templates:
            with open(os.path.join(self._root(), self.dist_dir, template), "w") as f2:
                slug = env.get_template(template)
                slug = slug.render(**kwargs)
                f2.write(slug)
        return True


if __name__ == "__main__":
    nav_entries = {
        "index.html": "Home",
        "research.html": "Research",
        "teaching.html": "Teaching",
        "publications.html": "Publications",
        "#contact": "Contact",
    }
    sb = SourceBundle(templates=["index.html"])
    sb.build(nav_entries=nav_entries, active_page="Home")

    courses = [
        "18/FA-INFO-601-04 Foundations of Information",
        "19/SP-INFO-601-02 Foundations of Information",
        "18/FA-INFO-673-01 Literacy & Instruction",
        "19/SP-INFO-697-05 Special Topics",
    ]
    sb = SourceBundle(templates=["teaching.html"])
    sb.build(nav_entries=nav_entries, active_page="Teaching", courses=courses)

    publications = [
        {
            "authors": "Bowler, L., Oh, J.S., & He, D.",
            "year": 2015,
            "title": "Teen Health Information Behavior and Social Q & A: A Study to Investigate Teens’ Assessments of the Accuracy, Credibility, and Reliability of Health Information about Eating Disorders",
            "link": "/static/sample.pdf",
            "venue": "Yahoo! Answers. ALISE 2015. January 27-30, 2015",
            "location": "Chicago, IL, USA",
        }
    ]
    publications = publications * 10

    sb = SourceBundle(templates=["publications.html"])
    sb.build(
        nav_entries=nav_entries, active_page="Publications", publications=publications
    )

    projects = [
        {
            "title": "Project Title",
            "img": "teaching-head.png",
            "desc": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam tristique nunc in odio volutpat accumsan. Interdum et malesuada fames ac ante ipsum primis in faucibus. In nisi erat, tristique vitae ipsum malesuada, aliquet posuere dui. Suspendisse sed sapien eget sem tempus maximus. Duis in nisl semper, placerat quam aliquet, gravida libero. Morbi sit amet placerat orci. Quisque tincidunt sed arcu nec laoreet. Morbi gravida sem lectus. Sed tincidunt, mi quis sagittis consequat, quam lacus egestas dolor, vitae tempor quam nulla vel ipsum. Aenean volutpat dictum ligula, et ultricies ligula tempus sed. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Etiam neque turpis, cursus sed massa et, accumsan imperdiet risus. Vivamus hendrerit leo ultrices tortor pretium, imperdiet consequat erat suscipit. Maecenas et odio velit.",
        }
    ]
    projects = projects * 10

    sb = SourceBundle(templates=["research.html"])
    sb.build(nav_entries=nav_entries, active_page="Research", projects=projects)

