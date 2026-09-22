typedef struct {
    char name[17];
    char contact[32];
    char linkedin[50];
    char github[50];
} growing_engineer_t;

growing_engineer_t me = {
    "Anissh Guruprasad",
    "anisshachar [at] gmail [dot] com",
    "https://www.linkedin.com/in/anissh-guru/",
    "https://github.com/ifndef-define"
};

/* Python
class GrowingEngineer:
    name = "Anissh Guruprasad"
    contact = "anisshachar [at] gmail [dot] com"
    linkedin = "https://www.linkedin.com/in/anissh-guru/"
    github = "https://github.com/ifndef-define"

me = GrowingEngineer()
*/

/* SystemVerilog
typedef struct {
    string name;
    string contact;
    string linkedin;
    string github;
} growing_engineer_t;

growing_engineer_t me = '{
    name: "Anissh Guruprasad",
    contact: "anisshachar [at] gmail [dot] com",
    linkedin: "https://www.linkedin.com/in/anissh-guru/",
    github: "https://github.com/ifndef-define"
};

// Example connectivity and state logic.
logic        clk;
logic        reset_n;
logic        profile_valid;
logic        profile_ready;
wire         profile_active = profile_valid & profile_ready;
logic [7:0]  profile_count;

always_ff @(posedge clk or negedge reset_n) begin
    if (!reset_n) begin
        profile_valid <= 1'b0;
        profile_count <= '0;
    end else begin
        profile_valid <= 1'b1;
        if (profile_active)
            profile_count <= profile_count + 8'd1;
    end
end

assign profile_ready = (profile_count != 8'hff);
*/

/* Assembly (NASM, x86-64)
section .data
name     db "Anissh Guruprasad", 0
contact  db "anisshachar [at] gmail [dot] com", 0
linkedin db "https://www.linkedin.com/in/anissh-guru/", 0
github   db "https://github.com/ifndef-define", 0
*/

#ifndef GROWING_ENGINEER
#define GROWING_ENGINEER

portfolio_t me = {
  "Anissh Guruprasad",
  // Hyperlinked Below!
  "anisshachar [at] gmail [dot] com",
  "linkedin.com/in/anissh-guru/",
  "github.com/ifndef-define"
};

about_me_t new_engineer = {
  "University of Illinois Urbana-Champaign",
  "B.S. in Computer Engineering",
  "Expected Graduation: May 2028",
  "Project-based learning and experience in" 
  " software development, embedded systems, and" 
  " hardware design.",
}

printf(to_resume(&me, &new_engineer) + "\n");
#endif // GROWING_ENGINEER