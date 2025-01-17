from job_manager import append_event
from agents import CompanyResearchAgents
from tasks import CompanyResearchTask
from crewai import Crew

class CompanyResearchCrew:
    def __init__(self, job_id: str):
        self.job_id = job_id
        self.crew = None

    def setup_crew(self, companies: list[str], positions: list[str]):
        agents = CompanyResearchAgents()
        research_manager = agents.research_manager(companies, positions)
        company_research_agent = agents.company_research_agent()

        tasks = CompanyResearchTask()

        company_research_task = [
            tasks.company_research(company_research_agent, company, positions) for company in companies
        ]

        manage_research = tasks.manager_research(research_manager, companies, positions, company_research_task)

        self.crew = Crew(
            name="Company Research Crew",
            agents=[research_manager, company_research_agent],
            tasks=[*company_research_task, manage_research],
            verbose=True
        )
        return 

    def kickoff(self):
        if not self.crew:
            print(f"No crew found for {self.job_id}")
            return
        
        append_event(self.job_id, "Starting crew")

        try:
            print(f"Running crew for {self.job_id}")
            results = self.crew.kickoff()
            append_event(self.job_id, "Crew finished")
            return results
        
        except Exception as e:
            return str(e)