import os
import openai

"""
Before submitting the assignment, describe here in a few sentences what you would have built next if you spent 2 more hours on this project:

"""

def call_model(prompt: str, max_tokens=3000, temperature=0.1) -> str:
    openai.api_key = os.getenv("OPENAI_API_KEY") # please use your own openai api key here.
    resp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        stream=False,
        max_tokens=max_tokens,
        temperature=temperature,
    )
    return resp.choices[0].message["content"]  # type: ignore

def judge_story(story: str) -> tuple[int, str]:
    """
    Evaluate a story and return (score, feedback).
    Score is 1-10, feedback explains what needs improvement.
    """
    judge_prompt = f"""You are an expert editor of children's bedtime stories for ages 5-10.

Evaluate the following story on these criteria:
1. Age-appropriateness (language, themes, complexity)
2. Story structure (clear beginning, middle, end)
3. Engagement (interesting for kids)
4. Length (appropriate for bedtime, ~300-500 words)

Story to evaluate:
{story}

Provide:
- A score from 1-10 (10 = perfect bedtime story)
- Specific feedback on what could be improved

Format your response as:
Score: [number]
Feedback: [your detailed feedback]"""

    response = call_model(judge_prompt, max_tokens=500, temperature=0.3)
    
    # Parse score and feedback from response
    lines = response.strip().split('\n')
    score = 5  # default
    feedback = ""
    
    for line in lines:
        if line.startswith("Score:"):
            try:
                score = int(line.split(":")[1].strip())
            except:
                pass
        elif line.startswith("Feedback:"):
            feedback = line.split(":", 1)[1].strip()
    
    return score, feedback

def generate_bedtime_story(user_request: str, max_iterations=3) -> str:
    """
    Generate a bedtime story with iterative refinement based on judge feedback.
    """
    storyteller_prompt = f"""You are a creative storyteller specializing in bedtime stories for children ages 5-10.

Your stories should:
- Use simple, age-appropriate language
- Follow a clear story arc: beginning, middle, end
- Be engaging and imaginative
- Include a positive message or gentle life lesson
- Be around 300-500 words
- Avoid scary, violent, or overly complex themes

Story request: {user_request}

Write a complete bedtime story based on this request."""

    story = call_model(storyteller_prompt, max_tokens=1000, temperature=0.7)
    
    for i in range(max_iterations):
        score, feedback = judge_story(story)
        print(f"\n[Iteration {i+1}] Judge score: {score}/10")
        print(f"Feedback: {feedback}\n")
        
        if score >= 8:
            print("Story approved by judge!\n")
            break
        
        # Refine story based on feedback
        refine_prompt = f"""Original story request: {user_request}

Current story:
{story}

Editor feedback: {feedback}

Please revise the story based on this feedback while keeping it appropriate for ages 5-10."""
        
        story = call_model(refine_prompt, max_tokens=1000, temperature=0.7)
    
    return story

example_requests = "A story about a girl named Alice and her best friend Bob, who happens to be a cat."


def main():
    user_input = input("What kind of story do you want to hear? ")
    story = generate_bedtime_story(user_input)
    print("\n" + "="*50)
    print("FINAL STORY:")
    print("="*50 + "\n")
    print(story)


if __name__ == "__main__":
    main()