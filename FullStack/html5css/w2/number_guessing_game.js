var target;
var guess_input_text;
var guess_input;
var finished = false;
var guesses = 0;


function do_game() {
  target = 1 + Math.floor(Math.random() * 100);
  while (!finished) {
    guess_input_text = prompt("I am thinking of a number "+
                                "in the range from 1 to 100.\n\n"+
                                "What is the number?");
    guess_input = parseInt(guess_input_text);
    guesses++;
    finished = check_guess();
  }
}

function check_guess() {
  if (isNaN(guess_input)) {
    alert("You have not entered a number.\n\n"+
          "Please enter a number in the range from 1 to 100.");
    return false;
  }
  if (guess_input < 1 || guess_input > 100) {
    alert("Please enter an integer in the range from 1 to 100.");
    return false;
  }
  if (guess_input > target) {
    alert("Your number is too large! Guess again.");
    return false;
  }
  if (guess_input < target) {
    alert("Your number is too small! Guess again.");
    return false;
  }

  alert("You got it! The number was "+target +
        "\nIt took you " + guesses + " guesses to get it.");
  return true;
}
