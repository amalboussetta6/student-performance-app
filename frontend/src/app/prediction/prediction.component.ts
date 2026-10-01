import { Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';


/* =========================================================
   INTERFACES
   ========================================================= */

interface StudentData {
  gender: string;
  study_hours_per_week: number;
  attendance_rate: number;
  past_exam_scores: number;
  parental_education_level: string;
  internet_access_at_home: string;
  extracurricular_activities: string;
}


interface Recommendation {
  variable: string;
  message: string;

  current_value: number;
  tested_value: number;

  estimated_gain: number;
}


interface PredictionResponse {
  predicted_score: number;
  result: string;
  recommendations: Recommendation[];
}


interface FeatureImportance {
  variable: string;
  importance: number;
}


interface ChatMessage {
  sender: 'user' | 'assistant';
  text: string;
}


interface ChatResponse {
  answer: string;
}


interface SimilarProfile {
  study_hours_per_week: number;
  attendance_rate: number;
  past_exam_scores: number;
  final_exam_score: number;
  result: string;
}


interface SimilarProfilesResponse {
  number_of_profiles: number;
  average_score: number;
  pass_rate: number;
  profiles: SimilarProfile[];
}


/* =========================================================
   COMPONENT
   ========================================================= */

@Component({
  selector: 'app-prediction',

  imports: [
    FormsModule,
    CommonModule
  ],

  templateUrl: './prediction.component.html',
  styleUrl: './prediction.component.css'
})

export class PredictionComponent implements OnInit {

  /* =======================================================
     CONFIGURATION API
     ======================================================= */

  private readonly apiUrl =
    'http://127.0.0.1:8000';


  /* =======================================================
     TITRE
     ======================================================= */

  title = 'Prédiction de la performance';


  /* =======================================================
     DONNÉES DU FORMULAIRE
     ======================================================= */

  gender = 'Male';

  studyHoursPerWeek = 0;

  attendanceRate = 0;

  pastExamScores = 0;

  parentalEducationLevel = 'High School';

  internetAccessAtHome = 'Yes';

  extracurricularActivities = 'Yes';


  /* =======================================================
     RÉSULTAT DE PRÉDICTION
     ======================================================= */

  predictedScore: number | null = null;

  result = '';

  errorMessage = '';

  isLoading = false;


  /* =======================================================
     IMPORTANCE DES VARIABLES
     ======================================================= */

  featureImportances: FeatureImportance[] = [];


  /* =======================================================
     RECOMMANDATIONS PERSONNALISÉES
     ======================================================= */

  recommendations: Recommendation[] = [];


  /* =======================================================
     CHATBOT
     ======================================================= */

  chatQuestion = '';

  chatLoading = false;

  chatMessages: ChatMessage[] = [];


  /* =======================================================
     PROFILS SIMILAIRES
     ======================================================= */

  similarProfiles: SimilarProfile[] = [];

  similarAverageScore: number | null = null;

  similarPassRate: number | null = null;

  similarProfilesLoading = false;


  /* =======================================================
     CONSTRUCTEUR
     ======================================================= */

  constructor(
    private http: HttpClient
  ) {

  }


  /* =======================================================
     INITIALISATION
     ======================================================= */

  ngOnInit() {

    this.loadFeatureImportances();

  }


  /* =======================================================
     CONSTRUIRE LES DONNÉES ÉTUDIANT
     ======================================================= */

  buildStudentData(): StudentData {

    return {

      gender:
        this.gender,

      study_hours_per_week:
        this.studyHoursPerWeek,

      attendance_rate:
        this.attendanceRate,

      past_exam_scores:
        this.pastExamScores,

      parental_education_level:
        this.parentalEducationLevel,

      internet_access_at_home:
        this.internetAccessAtHome,

      extracurricular_activities:
        this.extracurricularActivities

    };

  }


  /* =======================================================
     PRÉDICTION
     ======================================================= */

  predict() {

    this.errorMessage = '';

    this.predictedScore = null;

    this.result = '';

    this.recommendations = [];


    this.similarProfiles = [];

    this.similarAverageScore = null;

    this.similarPassRate = null;


    /* -----------------------------------------------------
       Validation du formulaire
       ----------------------------------------------------- */

    if (this.studyHoursPerWeek < 0) {

      this.errorMessage =
        "Les heures d'étude ne peuvent pas être négatives.";

      return;

    }


    if (
      this.attendanceRate < 0 ||
      this.attendanceRate > 100
    ) {

      this.errorMessage =
        "Le taux de présence doit être entre 0 et 100.";

      return;

    }


    if (
      this.pastExamScores < 0 ||
      this.pastExamScores > 100
    ) {

      this.errorMessage =
        "Le score précédent doit être entre 0 et 100.";

      return;

    }


    const studentData =
      this.buildStudentData();


    this.isLoading = true;


    /* -----------------------------------------------------
       Appel API /predict
       ----------------------------------------------------- */

    this.http.post<PredictionResponse>(
      `${this.apiUrl}/predict`,
      studentData
    )
    .subscribe({

      next: (response) => {

        this.predictedScore =
          response.predicted_score;

        this.result =
          response.result;


        /*
         * Les recommandations contiennent maintenant :
         *
         * variable
         * message
         * current_value
         * tested_value
         * estimated_gain
         */

        this.recommendations =
          response.recommendations || [];


        /* Réinitialiser le chatbot */

        this.chatMessages = [];

        this.chatQuestion = '';


        this.isLoading = false;


        /* Charger les étudiants similaires */

        this.loadSimilarProfiles();

      },


      error: (error) => {

        this.isLoading = false;

        this.errorMessage =
          "Impossible de récupérer la prédiction depuis le serveur.";

        console.error(
          'Erreur API :',
          error
        );

      }

    });

  }


  /* =======================================================
     IMPORTANCE DES VARIABLES
     ======================================================= */

  loadFeatureImportances() {

    this.http.get<{
      features: FeatureImportance[]
    }>(
      `${this.apiUrl}/feature-importance`
    )
    .subscribe({

      next: (response) => {

        this.featureImportances =
          response.features || [];

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


  /* =======================================================
     NOM LISIBLE D'UNE VARIABLE
     ======================================================= */

  getFeatureLabel(
    variable: string
  ): string {

    const labels: {
      [key: string]: string
    } = {

      gender:
        'Genre',

      study_hours_per_week:
        "Heures d'étude",

      attendance_rate:
        'Taux de présence',

      past_exam_scores:
        'Scores précédents',

      parental_education_level:
        'Éducation des parents',

      internet_access_at_home:
        'Accès à Internet',

      extracurricular_activities:
        'Activités extrascolaires'

    };


    return labels[variable] || variable;

  }


  /* =======================================================
     UNITÉ D'UNE RECOMMANDATION
     ======================================================= */

  getRecommendationUnit(
    variable: string
  ): string {

    if (variable === 'attendance_rate') {

      return '%';

    }


    if (
      variable ===
      'study_hours_per_week'
    ) {

      return 'h/semaine';

    }


    return '';

  }


  /* =======================================================
     POURCENTAGE POUR LE GRAPHIQUE
     ======================================================= */

  getImportancePercentage(
    importance: number
  ): number {

    if (
      this.featureImportances.length === 0
    ) {

      return 0;

    }


    const maxImportance =
      Math.max(
        ...this.featureImportances.map(
          feature =>
            Math.max(
              feature.importance,
              0
            )
        )
      );


    if (maxImportance === 0) {

      return 0;

    }


    return Math.max(
      0,
      (
        importance /
        maxImportance
      ) * 100
    );

  }


  /* =======================================================
     CHATBOT
     ======================================================= */

  sendChatMessage() {

    /* Vérifier qu'une prédiction existe */

    if (this.predictedScore === null) {

      this.chatMessages.push({

        sender: 'assistant',

        text:
          "Veuillez d'abord effectuer une prédiction."

      });

      return;

    }


    /* Nettoyer la question */

    const question =
      this.chatQuestion.trim();


    /* Ne rien envoyer si vide */

    if (question === '') {

      return;

    }


    /* Ajouter le message utilisateur */

    this.chatMessages.push({

      sender: 'user',

      text: question

    });


    /* Vider le champ */

    this.chatQuestion = '';


    this.chatLoading = true;


    /* -----------------------------------------------------
       Préparer les données chatbot
       ----------------------------------------------------- */

    const chatData = {

      question:
        question,

      predicted_score:
        this.predictedScore,

      result:
        this.result,

      /*
       * Important :
       *
       * recommendations contient désormais
       * current_value + tested_value +
       * estimated_gain.
       *
       * Le chatbot backend peut donc les utiliser.
       */

      recommendations:
        this.recommendations,

      student:
        this.buildStudentData()

    };


    /* -----------------------------------------------------
       Appel API /chat
       ----------------------------------------------------- */

    this.http.post<ChatResponse>(
      `${this.apiUrl}/chat`,
      chatData
    )
    .subscribe({

      next: (response) => {

        this.chatMessages.push({

          sender: 'assistant',

          text:
            response.answer

        });


        this.chatLoading = false;

      },


      error: (error) => {

        this.chatMessages.push({

          sender: 'assistant',

          text:
            "Une erreur est survenue lors de la communication avec l'assistant."

        });


        this.chatLoading = false;


        console.error(
          'Erreur chatbot :',
          error
        );

      }

    });

  }


  /* =======================================================
     PROFILS SIMILAIRES
     ======================================================= */

  loadSimilarProfiles() {

    this.similarProfilesLoading = true;


    const studentData =
      this.buildStudentData();


    this.http.post<SimilarProfilesResponse>(
      `${this.apiUrl}/similar-profiles`,
      studentData
    )
    .subscribe({

      next: (response) => {

        this.similarProfiles =
          response.profiles || [];


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