//// filepath: c:\Users\Yusuf\Documents\Bachelor\Code\frontend\Bachelor\src\app\pages\predict-water\predict-water.component.ts
import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { ApiService } from '../../api/api.service';
import { NONE_TYPE } from '@angular/compiler';

@Component({
  selector: 'app-predict-water',
  standalone: true,
  imports: [CommonModule, FormsModule, HttpClientModule],
  templateUrl: './predict-water.component.html',
  template: `<h1>Predict Water Works!</h1>`,
  styleUrls: ['./predict-water.component.css'],
})
export class PredictWaterComponent implements OnInit {
  triedSubmit = false;
  showAssistant = false;
  errorMessage: string | null = null;

  // Tracks loading status for each model
  modelsLoading: Record<string, boolean> = {
    DNN: false,
    DT: false,
    RF: false,
    SARIMAX: false,
    SVM: false,
    XGBoost: false,
    actual: false, // 'actual' not auto-loaded
  };

  form = {
    date: '', // Sets the date to tomorrow in 'YYYY-MM-DD' format
    location: '',
    crop_type: '',
    soil_type: '',
    season: '',
    area: 0,
    initial_moisture: 0,
    max_moisture: 0,
  };
  // form = {
  //   date: new Date(new Date().setDate(new Date().getDate() + 1))
  //     .toISOString()
  //     .split('T')[0], // Sets the date to tomorrow in 'YYYY-MM-DD' format
  //   location: 'Cairo',
  //   crop_type: 'Olive',
  //   soil_type: 'Clay',
  //   season: 'Mid-season',
  //   area: 1000,
  //   initial_moisture: 10,
  //   max_moisture: 20,
  // };

  results: {
    DNN: string | null;
    DT: string | null;
    RF: string | null;
    SARIMAX: string | null;
    SVM: string | null;
    XGBoost: string | null;
    actual: string | null;
    DNN_accuracy?: string | null;
    DT_accuracy?: string | null;
    RF_accuracy?: string | null;
    SARIMAX_accuracy?: string | null;
    SVM_accuracy?: string | null;
    XGBoost_accuracy?: string | null;
    actual_accuracy?: string | null;
  } = {
    DNN: null,
    DT: null,
    RF: null,
    SARIMAX: null,
    SVM: null,
    XGBoost: null,
    actual: null,
    DNN_accuracy: null,
    DT_accuracy: null,
    RF_accuracy: null,
    SARIMAX_accuracy: null,
    SVM_accuracy: null,
    XGBoost_accuracy: null,
    actual_accuracy: null,
  };

  constructor(private api: ApiService) {}
  ngOnInit(): void {
    //this.loadModel('DT');
  }

  loadModel(model: string) {
    this.api.loadModel(model.toLowerCase()).subscribe({
      next: () => {},
      error: () => {
        this.errorMessage = `Error loading ${model} model`;
      },
      complete: () => {
        this.modelsLoading[model] = false;
      },
    });
  }

  isValid(): boolean {
    return Boolean(
      this.form.date &&
        this.form.location &&
        this.form.crop_type &&
        this.form.soil_type &&
        this.form.season &&
        this.form.area > 0 &&
        this.form.initial_moisture > 0 &&
        this.form.max_moisture > this.form.initial_moisture
    );
  }

  runModel(model: string) {
    this.triedSubmit = true;
    if (!this.isValid()) {
      this.errorMessage = 'Please fill in all fields correctly.';
      return;
    }
    this.modelsLoading[model] = true;
    this.errorMessage = "Sometimes it takes maybe 4 minutes to load the model, please be patient";

    // Optional: set a local loading flag if desired
    this.api.predict(model.toLowerCase(), this.form).subscribe({
      next: (response) => {
        // If backend returns null for the prediction
        if (response.amount == null) {
          this.errorMessage = 'Enter a valid date in the next 12 days';
          return;
        }
        this.errorMessage = null;
        const predicted = parseFloat(response.amount).toFixed(2);
        this.results[model as keyof typeof this.results] = predicted;

        // If actual is present, compute accuracy
        if (model !== 'actual' && this.results.actual) {
          const actualVal = parseFloat(this.results.actual);
          const accuracy =
            100 * (1 - Math.abs(actualVal - parseFloat(predicted)) / actualVal);
          this.results[`${model}_accuracy` as keyof typeof this.results] =
            accuracy.toFixed(2);
        }
        if(model === 'actual') {
            Object.keys(this.results).forEach((key) => {
            if (key !== 'actual' && this.results[key as keyof typeof this.results]) {
              const predictedVal = parseFloat(this.results[key as keyof typeof this.results] as string);
              const actualVal = parseFloat(predicted);
              const accuracy =
              100 * (1 - Math.abs(actualVal - predictedVal) / actualVal);
              this.results[`${key}_accuracy` as keyof typeof this.results] =
              accuracy.toFixed(2);
            }
            });
        }
      },
      error: () => {
        this.errorMessage = 'An error occurred.';
      },
      complete: () => {
        this.modelsLoading[model] = false;
      },

    });
  }
}