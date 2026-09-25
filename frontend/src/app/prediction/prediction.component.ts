import { Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-prediction',
  imports: [FormsModule, CommonModule],
  templateUrl: './prediction.component.html',
  styleUrl: './prediction.component.css'
})
export class PredictionComponent implements OnInit {

  title = 'Prédiction de la performance';

  gender = 'Male';
  studyHoursPerWeek = 0;
  attendanceRate = 0;
  pastExamScores = 0;
  parentalEducationLevel = 'High School';
  internetAccessAtHome = 'Yes';
  extracurricularActivities = 'Yes';

  predictedScore: number | null = null;
  result = '';
  errorMessage = '';
  isLoading = false;

  featureImportances: any[] = [];
  recommendations: any[] = [];

  chatQuestion = '';
  chatLoading = false;

  chatMessages: {
    sender: 'user' | 'assistant';
    text: string;
}[] = [];

  similarProfiles: any[] = [];

  similarAverageScore: number | null = null;

  similarPassRate: number | null = null;

  similarProfilesLoading = false;

  constructor(private http: HttpClient) {

  }

predict() {

  this.errorMessage = '';

  this.predictedScore = null;
  this.result = '';

  this.recommendations = [];

  this.similarProfiles = [];
  this.similarAverageScore = null;
  this.similarPassRate = null;

  if (this.studyHoursPerWeek < 0) {
    this.errorMessage = "Les heures d'étude ne peuvent pas être négatives.";
    return;
  }

  if (this.attendanceRate < 0 || this.attendanceRate > 100) {
    this.errorMessage = "Le taux de présence doit être entre 0 et 100.";
    return;
  }

  if (this.pastExamScores < 0 || this.pastExamScores > 100) {
    this.errorMessage = "Le score précédent doit être entre 0 et 100.";
    return;
  }

  const studentData = {
    gender: this.gender,
    study_hours_per_week: this.studyHoursPerWeek,
    attendance_rate: this.attendanceRate,
    past_exam_scores: this.pastExamScores,
    parental_education_level: this.parentalEducationLevel,
    internet_access_at_home: this.internetAccessAtHome,
    extracurricular_activities: this.extracurricularActivities
  };

    this.isLoading = true;

    this.http.post(
      'http://127.0.0.1:8000/predict',
      studentData
    ).subscribe({

      next: (response: any) => {

        this.predictedScore = response.predicted_score;
        this.result = response.result;

        this.recommendations = response.recommendations || [];

        this.chatMessages = [];
        this.chatQuestion = '';

        this.isLoading = false;

        this.loadSimilarProfiles();
      },

      error: (error) => {

        this.isLoading = false;

        this.errorMessage =
          "Impossible de récupérer la prédiction depuis le serveur.";

        console.error('Erreur API :', error);
      }

    });
    }

loadFeatureImportances() {

      this.http.get<any>(
        'http://127.0.0.1:8000/feature-importance'
      ).subscribe({

        next: (response) => {

          this.featureImportances = response.features;

          console.log(
            'Importance des variables :',
            this.featureImportances
          );
        },

        error: (error) => {

          console.error(
            "Erreur lors du chargement des importances :",
            error
          );
        }

      });
    }
getFeatureLabel(variable: string): string {

  const labels: { [key: string]: string } = {
    gender: 'Genre',
    study_hours_per_week: "Heures d'étude",
    attendance_rate: 'Taux de présence',
    past_exam_scores: 'Scores précédents',
    parental_education_level: 'Éducation des parents',
    internet_access_at_home: 'Accès à Internet',
    extracurricular_activities: 'Activités extrascolaires'
  };

  return labels[variable] || variable;
}
getImportancePercentage(importance: number): number {

  if (this.featureImportances.length === 0) {
    return 0;
  }

  const maxImportance = Math.max(
    ...this.featureImportances.map(
      feature => Math.max(feature.importance, 0)
    )
  );

  if (maxImportance === 0) {
    return 0;
  }

  return Math.max(
    0,
    (importance / maxImportance) * 100
  );
}
ngOnInit() {
  this.loadFeatureImportances();
}

sendChatMessage() {

  // Vérifier qu'une prédiction existe
  if (this.predictedScore === null) {

    this.chatMessages.push({
      sender: 'assistant',
      text: "Veuillez d'abord effectuer une prédiction."
    });

    return;
  }


  // Récupérer la question et enlever les espaces inutiles
  const question = this.chatQuestion.trim();


  // Ne rien envoyer si la question est vide
  if (question === '') {
    return;
  }


  // Ajouter la question de l'utilisateur à l'historique
  this.chatMessages.push({
    sender: 'user',
    text: question
  });


  // Vider le champ après l'envoi
  this.chatQuestion = '';


  // Activer le chargement
  this.chatLoading = true;


  // Préparer les données envoyées à FastAPI
  const chatData = {
    question: question,
    predicted_score: this.predictedScore,
    result: this.result,
    recommendations: this.recommendations
  };


  // Envoyer la question au backend
  this.http.post<any>(
    'http://127.0.0.1:8000/chat',
    chatData
  ).subscribe({

    next: (response) => {

      // Ajouter la réponse de l'assistant à l'historique
      this.chatMessages.push({
        sender: 'assistant',
        text: response.answer
      });

      this.chatLoading = false;
    },

    error: (error) => {

      this.chatMessages.push({
        sender: 'assistant',
        text: "Une erreur est survenue lors de la communication avec l'assistant."
      });

      this.chatLoading = false;

      console.error(
        'Erreur chatbot :',
        error
      );
    }

  });
}

loadSimilarProfiles() {

  this.similarProfilesLoading = true;

  const studentData = {
    gender: this.gender,
    study_hours_per_week: this.studyHoursPerWeek,
    attendance_rate: this.attendanceRate,
    past_exam_scores: this.pastExamScores,
    parental_education_level: this.parentalEducationLevel,
    internet_access_at_home: this.internetAccessAtHome,
    extracurricular_activities: this.extracurricularActivities
  };

  this.http.post<any>(
    'http://127.0.0.1:8000/similar-profiles',
    studentData
  ).subscribe({

    next: (response) => {

      this.similarProfiles = response.profiles;

      this.similarAverageScore =
        response.average_score;

      this.similarPassRate =
        response.pass_rate;

      this.similarProfilesLoading = false;

      console.log(
        'Profils similaires :',
        response
      );
    },

    error: (error) => {

      this.similarProfilesLoading = false;

      console.error(
        'Erreur profils similaires :',
        error
      );
    }

  });
}
}

