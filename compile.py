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

    # publications = [
    #     {
    #         "authors": "Bowler, L., Oh, J.S., & He, D.",
    #         "year": 2015,
    #         "title": "Teen Health Information Behavior and Social Q & A: A Study to Investigate Teens' Assessments of the Accuracy, Credibility, and Reliability of Health Information about Eating Disorders",
    #         "link": "/static/sample.pdf",
    #         "venue": "Yahoo! Answers. ALISE 2015. January 27-30, 2015",
    #         "location": "Chicago, IL, USA",
    #     }
    # ]
    publications = [
        "Bowler, L., Julien, H. & Haddon, L. (2018). Exploring youth information-seeking behaviour and mobile technologies through a secondary analysis of qualitative data. Journal of Librarianship and Information Science, Vol. 50(3) 322-331. 	",
        "Chi, Y., Jeng, W., Acker, A., & Bowler, L. (2018, March). Affective, Behavioral, and Cognitive Aspects of Teen Perspectives on Personal Data in Social Media: A Model of Youth Data Literacy. In International Conference on Information (pp. 442-452). Springer, Cham.	",
        "Acker, A. & Bowler, L. (2018).  Youth Data Literacy: Teen Perspectives on Data Created with Social Media, and Mobile Device Ownership. Hawaii International Conference on System Sciences 2018 (HICCS). January 3-6, 2018. ",
        "Bowler, L., Acker, A., Jeng, W. & Chi, Y. (2017). \"It lives all around us\": Aspects of Data Literacy in Teens' Lives.  80th ASIS&T Annual Meeting. Diversity of Engagement: Connecting People and Information in the Physical and Virtual Worlds. October 27-November 1, 2017. Washington, D.C. ",
        "Acker, A. & Bowler, L. (2017). What is Your Data Silhouette? Raising Teen Awareness of their Data Traces in Social Media. Social Media and Society International Conference, July 28-30, 2017. ",
        "Bowler, L. & Champagne, R. (2016). Mindful making: Question prompts to help guide young peoples' critical technical practices in DIY/maker spaces. Library and Information Science Research, 38, 117-124.  ",
        "Fan, M., Liyue, Y. & Bowler, L. (2016). Feelbook: A Social Media App For Teens Designed To Foster Positive Online Behavior And Prevent Cyberbullying. CHI 2016, May 7-12, 2015, San Jose, CA. ",
        "Bowler, L., Monahan, J., Jeng, W., Oh, J. & He, D. (2015). The quality and helpfulness of answers to eating disorder questions in Yahoo! Answers: Teens speak out. 78th ASIS&T Annual Meeting, Information Science with Impact: Research in and for the Community. November 6-10, 2015. St. Louis, MO.",
        "Bowler, L., Knobel, C. & Mattern, E. (2015). From cyberbullying to well-being: A narrative-based participatory approach to values-oriented design themes for social media. Journal of the Association for Information Science and Technology, 66(6), 1274-1293. ",
        "Bowler, L. (2014). Creativity through \"Maker\" experiences and design thinking in the education of librarians. Knowledge Quest: Journal of the American Association of School Librarians. 42(5), May-June, pp. 59-61.",
        "Bowler, L., Mattern, E., & Knobel, C. (2014). Developing design interventions for cyberbullying: A narrative-based participatory approach. iConference 2014: Breaking Down Walls - Culture, Context, Computing, March 4-7, 2014. Berlin, Germany.",
        "Bowler, L., Mattern, E. Jeng, W., Oh, J. & He, D. (2013). \"I know what you are going through\": Answers to informational questions about eating disorders in Yahoo! Answers: A qualitative study. 2013 ASIS&T Annual Meeting, Rethinking Information Boundaries, November 1-6, 2013. Montreal, QC, Canada.",
        "Oh, J.S., Jeng, W., He, D., Mattern, E. & Bowler, L. (2013). Linguistic characteristics of eating disorder questions on Yahoo! Answers - content, style, and emotion. 2013 ASIS&T Annual Meeting, Rethinking Information Boundaries, November 1-6, 2013. Montreal, QC, Canada.",
        "Bowler, L. Oh, J.S., He, D., Mattern, E., & Jeing, W. (2012). Eating disorder questions in Yahoo! Answers: Information, conversation, or reflection? 2012 ASIS&T Annual Meeting, Information, Interaction, Innovation: Celebrating the Past, Constructing the Present and Creating the Future, October 28-31, 2012. Baltimore, MD.",
        "Bowler, L. & Mattern, E. (2012). Visual metaphors for modeling metacognitive strategies that support memory during the information search process. IIiX Fourth Information in Interaction in Context Symposium. August 21-24, 2012. Nijmegan, The Netherlands.",
        "Bowler, L. & Mattern, E. (2012). Design techniques for revealing adolescent memory processes related to information seeking: A preliminary study. iConference 2012: Culture, Design, Society. February 7, 2012. Toronto, ON, Canada.",
        "Bowler, L., Morris, R., Al-Issa, R., Cheng, I., Romine, B. and Leiberling, L. (2012). Multi-modal stories: LIS students explore reading, literacy, and library service through the lens of 'The 39 Clues.' Journal of Library and Information Science Education, 53(1), 32-48.",
        "Cox, R., Ceja, J. & Bowler, L. (2012). Archival document packets:  A teaching module in advocacy training using the papers of Governor Dick Thornburgh. The American Archivist, 75(2), 371-392.",
        "Bowler, L., He, D., & Hong, W. (2011). Who is referring teens to health information on the Web? Hyperlinks between blogs and teen health web sites for teens. iConference 2011: Inspiration, Integrity, Intrepidity. February 8-11, 2011. Seattle, WA.",
        "Bowler, L., Koshman, S., Oh, J. S., He, D., Callery, B., Bowker, G. & Cox, R. (2011). Issues in user-centered design in LIS (Special issue: Involving Users in the Co- Construction of Digital Knowledge in Libraries, Archives, and Museums). Library Trends, 59(4), 721-752.",
        "Bowler, L., Hong, W. Y. & He, D. (2011). The visibility of health web portals for teens: A hyperlink analysis. Online Information Review: The International Journal of Digital Information Research and Use, 35(3), 443 - 470.",
        "Bowler, L. (2010). A taxonomy of adolescent metacognitive knowledge during the information search process. Library and Information Science Research. 32(1): 27- 42.",
        "Bowler, L. (2010). Talk as a metacognitive strategy during the information search process of adolescents. Information Research, 15(4) paper 449.",
        "Bowler, L. (2010). The self-regulation of curiosity and interest during the information search process of adolescent students. Journal of the American Society for Information Science and Technology, 61(7), 1332-1344.",
        "Bowler, L. (2009). Dangerous Stories. English Quarterly, 39(2), pp. 53-55.",
        "Bowler, L. (2009). Genres of search: A concept for understanding successive search behaviour. Canadian Journal of Library and Information Science. 33(3/4): 119-140.",
        "Bowler, L. (2008). The metacognitive knowledge of adolescent students during the information search process. Information Beyond Borders: LIS interacting with other disciplines. Proceedings of the 36th Annual Conference of the Canadian Association for Information Science (CAIS), University of British Columbia. June 5-7, 2008. Vancouver, BC, Canada.",
        "Bowler, L. & Large, A. (2008). Design-based research for LIS. Library and Information Science Research. 30: 39-46.",
        "Bowler, L. (2007). Methods for revealing the metacognitive knowledge of adolescent information seekers during the information search process. Information Sharing in a Fragmented World: Crossing Boundaries. Proceedings of the 35th Annual Conference of the Canadian Association for Information Science. May 10 - 12, 2007. Montreal, QC, Canada.",
        "Large, A., Beheshti, J., Nesset, V., & Bowler, L. (2007). Children's representations of taxonomic categories for application in a web portal: An exploratory study. In C. Arsenault and K. Dalkir (Eds.), Information Sharing in a Fragmented World: Crossing Boundaries: Proceedings of the Canadian Association for Information Science (CAIS). May 10-12, 2007. Montreal, QC, Canada.",
        "Large, A., Bowler, L., Beheshti, J. & Nesset, V. (2007). Bonded Design, intergenerational teams and the Zone of Proximal Development: Working with children as designers. McGill Journal of Education, 42(1): 61- 82.",
        "Large, A. and Beheshti, J. and Nesset, V. and Bowler, L. (2006). Web Portal Design Guidelines as Identified by Children through the Processes of Design and Evaluation. Proceedings of the American Society for Information Science and Technology (ASIST). November 3-8, 2006. Austin, TX.",
        "Large, A., Beheshti, J., Nesset, V. & Bowler, L. (2006). \"Bonded Design\": A novel approach to intergenerational information technology design. Library and Information Science Research. 28: 64 - 82.",
        "Bowler, L. & Mittermeyer, D. (2006). Être bibliothécaire au XXIième siėcle: comment donner un sens à l'information. Documentation et bibliothèques.52(3). pp. 197-199. ",
        "Bowler, L., Large, A., Beheshti, J., & Nesset, V. (2005). Children and adults working together in the Zone of Proximal Development: A concept for user-centered design. In L. Vaughn, (Ed.), Data, Information, and Knowledge in a Networked World. Proceedings of the Canadian Society for Information Science and Technology. June 2-4, 2005. London, ON, Canada.",
        "Large, A., Beheshti, J., Nesset, V., & Bowler, L. (2005). Web portal characteristics: Children as designers and evaluators. In L. Vaughn, (Ed.), Data, Information, and Knowledge in a Networked World: Proceedings of the Canadian Society for Information Science and Technology. June 2-4, 2005, London, ON, Canada.",
        "Large, A., Beheshti, J., Nesset, V. & Bowler, L. (2004). Designing web portals in intergenerational teams: Two prototype portals for elementary school students. Journal of the American Society for Information Science and Technology, 55(13), pp. 1140-1154.",
        "Large, A, Nesset, V., Beheshti, J. & Bowler, L. (2004). Design criteria for children's web portals: A comparison of two studies. Canadian Journal of Library and Information Science. 28(4): 45-72.",
        "Bowler, L., Nesset, V., Large, A. & Beheshti, J., (2004). Using the web for Canadian history projects: What will children find? Canadian Journal of Library and Information Science. 28(3): 3 - 24.",
        "Large, A., Beheshti, J., Nesset, V., & Bowler, L. (2004). Children's web portals: Are adult designers on target? Access to Information: Technologies, Skills, and Socio- Political Context. Proceedings of the Canadian Society for Information Science. June 3-5, 2004, Winnipeg, MB, Canada.",
        "Large, A., Beheshti, J., Nesset, V., & Bowler, L. (2004). Designing a children's web portal using an intergenerational team. Proceedings PISTA 2004. International Conference on Politics and Information Systems: Technologies and Applications, Volume 1. July 21-25, 2004, Orlando, FL, (pp. 222-227). Orlando: International Institute of Informatics and Systemics.",
        "Large, A., Beheshti, J., Nesset, V., & Bowler, L. (2003). Children as web portal designers: Where do we start? Proceedings of the 31st Annual Conference of the Canadian Association for Information Science, May 30-June 1, Halifax, NS, Canada. (pp. 139-152).",
        "Large, A., Beheshti, J., Nesset, V., & Bowler, L. (2003). Children as designers of web portals. Humanizing Information Technology: From Ideas to Bits and Back: Proceedings of the 66th Annual Meeting of the American Society for Information Science and Technology, October 19-23, Long Beach, CA (pp. 142-149). Medford, NJ: Information Today.",
        "Bowler, L., Large, A. & Rejskind, G., (2001). Primary school students, information literacy, and the Web, Education for Information, 19, 201-223.",
    ]

    sb = SourceBundle(templates=["publications.html"])
    sb.build(
        nav_entries=nav_entries, active_page="Publications", publications=publications
    )

    projects = [
        {
            "title": "Exploring Data Worlds at the Public Library: A Youth Data Literacy Project",
            "img": "img/project1.png",
            "desc": "The Exploring Data Worlds at the Public Library research project is supported by a grant from the Institute for Museum and Library Services. Amelia Acker (UT Austin) and I have been exploring youth data literacy in the context of youth services in maker spaces at the public library. The goals of the Exploring Data Worlds project are threefold: 1) to generate social science observations about young peoples' interactions with data, including their self-awareness as data subjects, 2) to discover the unique data literacy needs of digital youth in terms of their critical and civic participation in a data driven society, and 3) develop strategies for training youth librarians in order to provide them with the skills to empower young people. See recent publications for details about youth data literacy, Chi, Y., Jeng, W., Acker, A., & Bowler, L., 2018; Acker, A. & Bowler, L., 2018; Bowler, L., Acker, A., Jeng, W. & Chi, Y., 2017; Acker, A. & Bowler, L., 2017.",
            "link": "https://www.youthdataliteracy.info/",
        },
        {
            "title": '"Mindful Making": Critical computing and informal STEM learning in Maker Spaces',
            "img": "img/project2.png",
            "desc": "This research program, originally supported through grants from the Sprout Foundation and the Association for Library and Information Science, investigates critical making, self-awareness, and the practice of self-critique in library-based maker spaces. See Bowler, 2016; Bowler, L. & Champagne, R., 2016, for more details.",
            "link": "http://www.mindfulmakerquestions.info/",
        },
        {
            "title": "Remake Making",
            "img": "",
            "desc": "A collaboration with principal investigator Tom Akiva (University of Pittsburgh), Kevin Crowley (University of Pittsburgh), and Peter Wardrip (University Wisconsin-Madison). The project is supported by a grant from the National Science Foundation. The study explores professional development and community-based, facilitation models in support of informal STEM learning at the public library.",
            "link": "https://www.simpleinteractions.org/ ",
        },
        {
            "title": '"Think Before You Click!" Designing Social Media Spaces that Afford Moments of Reflection (Study into Cyberbullying)',
            "img": "img/project4.png",
            "desc": "This project looked at mean and cruel online behavior through the lens of design, with the goal of developing positive technologies for youth. Visual narrative inquiry - a storytelling method - was used in the early stages of this project to explore the relationship between reflection (the metacognitive piece), values, and interaction design. Seven emergent design themes were evident in the participants' design recommendations and these design themes were then associated with a values-framework (Cheng & Fleishman, 2010). For more information, see Bowler, Knobel & Mattern, 2015; Fan, M., Liyue, Y. & Bowler, L., 2016.",
            "link": "",
        },
        {
            "title": "Social Q&A and Teen Health",
            "img": "",
            "desc": "This project began with the basic question, How do teens use social media to answer their health questions? Supported through a grant from OCLC, my colleagues Daqing He (University of Pittsburgh), Jung Sun Oh (University of Pittsburgh) and I looked at a health topic that is relevant to teens - eating disorders - in order to model the interactions between questioners and askers in the social Q&A space of Yahoo! Answers, with the aim of contributing to the greater understanding of youth information behavior, health information literacy, and the role of social Q&A and affect in the provision of health information to young people. See Bowler et al, 2012, 2013; Oh et al, 2013, for more information.",
            "link": "",
        },
    ]

    sb = SourceBundle(templates=["research.html"])
    sb.build(nav_entries=nav_entries, active_page="Research", projects=projects)

