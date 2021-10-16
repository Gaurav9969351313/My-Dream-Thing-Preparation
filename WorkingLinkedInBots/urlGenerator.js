var positionArray = [
  "IT Recruiter",
  "Headhunter",
  "talent management",
  "Recruiter",
  "Talent Manager",
  "Human Resource Manager",
  "Technical Recruiter",
  "IT Recruitment Consultant",
  "tech Recruiter",

  "Vice President of Human Resources",
  "HR",
  "Corporate Recruiter",
  "Executive Recruiter",
  "Recruitement Agency",
  "Talent Acquisition Manager",
  "recruiter",
  "Sr Recruiter",
  "HR Business Partner",
  "HR Generalist",
  "HR Consultant",
  "Human Resources Assistant",
  "HR Analyst"
  
  // ,
  // "HR Coordinator",
  // "Virtual Recruiter",
  // "Remote Human Resources",
  // "Training Coordinator",
  // "Payroll Clerk",
  // "Human Resources Generalist",
  // "Recruiting Coordinator",
  // "Benefits Specialist",
  // "Campus Recruiter",
  // "Benefits Administrator",
  // "Payroll Administrator",
  
  // "HRIS Analyst",
];

var countryArray = [
  "Australia",
  "Bahrain",
  "Bosnia",
  "Bulgaria",
  "Dubai ",
  "Estonia",
  "Israel",
  "jordan",
  "Kuwait",
  "Libia",
  "Mexico",
  "Netherlands",
  "New Zealand",
  "Oman",
  "Poland",
  "Qatar",
  "Singapore",
  "Switzerland",
  "United Arab Emirates",
  "United Kingdom",
  "Ireland"
];

var baseUrl = "https://www.google.com/search?q=";

// var ik = 0;
// for (let i = 0; i < countryArray.length; i++) {
//     var countryName = countryArray[i];
//     for (let j = 0; j < positionArray.length; j++) {
//         var positionName = positionArray[j];
//         var q = 'https://www.google.com/search?q="' + countryName + '"+' + '"Email"+AND+"' + positionName+ '"+site:linkedin.com';    
//         ik++

//         console.log(q);
//     }
// }
// console.log(ik);

var countryName = "oslo"; // countryArray[]
for (let i = 0; i < positionArray.length; i++) {
  const positionName = positionArray[i];
  var q = 'https://www.google.com/search?q="' + countryName + '"+' + '"Email"+AND+"' + positionName+ '"+site:linkedin.com';    
  console.log(q);
}
