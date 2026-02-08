from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse, RedirectResponse
from uvicorn import run as app_run

from typing import Optional

from src.constants import APP_HOST, APP_PORT
from src.pipline.prediction_pipeline import InsuranceData, InsuranceDataClassifier
from src.pipline.training_pipeline import TrainPipeline

app = FastAPI()

# Render the static file like CSS
app.mount("/static", StaticFiles(directory="static"), name="static")

# HTML file
templates = Jinja2Templates(directory="templates")

# Allow all origins for Cross-Origin Resource Sharing (CORS)
origins = ["*"]

# Configure middleware to handle CORS, allowing requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class DataForm:
    """
    DataForm class to handle and process incoming form data.
    This class defines the insurance-related attributes expected from the form.
    """

    def __init__(self, request: Request):
        self.request: Request = request

        # Policy Information
        self.policy_number: Optional[int] = None
        self.policy_annual_premium: Optional[float] = None
        self.months_as_customer: Optional[int] = None

        # Insured Information
        self.age: Optional[int] = None
        self.insured_zip: Optional[int] = None
        self.capital_gains: Optional[int] = None
        self.insured_occupation: Optional[str] = None
        self.insured_hobbies: Optional[str] = None

        # Incident Information
        self.incident_type: Optional[str] = None
        self.collision_type: Optional[str] = None
        self.incident_severity: Optional[str] = None
        self.incident_state: Optional[str] = None
        self.authorities_contacted: Optional[str] = None

        # Claims Information
        self.property_claim: Optional[int] = None
        self.vehicle_claim: Optional[int] = None
        self.injury_claim: Optional[int] = None
        self.total_claim_amount: Optional[int] = None

        # Fraud Status
        self.fraud_reported: Optional[str] = None

    async def get_insurance_data(self):
        """
        Method to retrieve and assign form data to class attributes.
        This method is asynchronous to handle form data fetching without blocking.
        """
        form = await self.request.form()

        # Policy Information
        self.policy_number = form.get("policy_number")
        self.policy_annual_premium = form.get("policy_annual_premium")
        self.months_as_customer = form.get("months_as_customer")

        # Insured Information
        self.age = form.get("age")
        self.insured_zip = form.get("insured_zip")
        self.capital_gains = form.get("capital-gains")
        self.insured_occupation = form.get("insured_occupation")
        self.insured_hobbies = form.get("insured_hobbies")

        # Incident Information
        self.incident_type = form.get("incident_type")
        self.collision_type = form.get("collision_type")
        self.incident_severity = form.get("incident_severity")
        self.incident_state = form.get("incident_state")
        self.authorities_contacted = form.get("authorities_contacted")

        # Claims Information
        self.property_claim = form.get("property_claim")
        self.vehicle_claim = form.get("vehicle_claim")
        self.injury_claim = form.get("injury_claim")
        self.total_claim_amount = form.get("total_claim_amount")

        # Fraud Status
        self.fraud_reported = form.get("fraud_reported")


# Route to render the main page with the form
@app.get("/", tags=["authentication"])
async def index(request: Request):
    return templates.TemplateResponse(
        "index.html", {"request": request, "context": "Rendering"}
    )


# Route to trigger the model training process
@app.get("/train")
async def trainRouteClient():
    """
    Endpoint to initiate the model training pipeline.
    """
    try:
        train_pipeline = TrainPipeline()
        train_pipeline.run_pipeline()
        return "Training successfully!!!!"

    except Exception as e:
        return Response(f"Error Occurred! {e}")


# Route to handle form submission and make predictions
@app.post("/")
async def predictionRouteClient(request: Request):
    """
    Endpoint to receive form data, process it, and make a fraud prediction.
    """

    try:
        form = DataForm(request)
        await form.get_insurance_data()

        insurance_data = InsuranceData(
            policy_number=form.policy_number,
            policy_annual_premium=form.policy_annual_premium,
            months_as_customer=form.months_as_customer,
            age=form.age,
            insured_zip=form.insured_zip,
            capital_gains=form.capital_gains,
            insured_occupation=form.insured_occupation,
            insured_hobbies=form.insured_hobbies,
            incident_type=form.incident_type,
            collision_type=form.collision_type,
            incident_severity=form.incident_severity,
            incident_state=form.incident_state,
            authorities_contacted=form.authorities_contacted,
            property_claim=form.property_claim,
            vehicle_claim=form.vehicle_claim,
            injury_claim=form.injury_claim,
            total_claim_amount=form.total_claim_amount,
            fraud_reported=form.fraud_reported
        )

        # Convert form data into a DataFrame for the model
        insurance_df = insurance_data.get_insurance_input_data_frame()

        # Initialize the prediction pipeline
        model_predictor = InsuranceDataClassifier()

        # Make a prediction and retrieve the result
        value = model_predictor.predict(dataframe=insurance_df)[0]

        # Interpret the prediction result
        status = "Fraud Detected" if value == 1 else "No Fraud Detected"

        # Render the same HTML page with the prediction result
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "context": status},
        )

    except Exception as e:
        return {"status": "False", "error": f"{e}"}


# Driver Code
if __name__ == "__main__":
    app_run(app, host=APP_HOST, port=APP_PORT)