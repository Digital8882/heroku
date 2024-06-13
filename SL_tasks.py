from crewai import Task

icp_task = Task(
    description=f"""Your task is to create a detailed ideal customer profile that will guide marketing and product development strategies for a business selling the product ."
            "To generate the ICP, consider the following:"
            "- Analyze the provided customer feedback, market research, and industry reports to identify patterns and insights about the target customer"
            "- Determine the demographic, geographic, and psychographic characteristics of the ideal customer"
            "- Identify the customer's pain points, needs, and challenges related to the product or service"
            "- Describe the customer's goals, desires, and aspirations that the product or service can help fulfill"
            "- Summarize the customer's preferred communication channels and media consumption habits"
            "- List the customer's most common objections and hesitations when considering a purchase of the product or service"
            "- Explore the factors that influence the customer's decision-making process when choosing a product or service in the relevant category"
            "- Create a memorable and relatable name for the ICP that reflects the target customer's characteristics or role (e.g., 'Marketing Manager Molly,' 'Fitness Enthusiast Frank')"
            "If the majority of the target customers are men, use a male example in the profile. If the majority are women, use a female example."
            "The ICP should be written in a professional, analytical tone, with clarity and accessibility necessary for understanding by team members across different functions."
            "Remember to regularly review and update the ICP based on new customer data, market trends, and product changes.""",
    expected_output=f""" Create an ideal customer profile document of approximately 1000 words , including:"
            "a story-like format that is easy to understand and remember. For example:"
            "Meet [Name], a [age]-year-old [gender] who works as a [occupation] in [location]. [Name] values [values] and enjoys [interests/hobbies] in their free time. As a [personality trait] person, [Name] struggles with [pain point/challenge] when it comes to [product/service category]. They aspire to [goal/desire] and believe that the right [product/service] can help them achieve this. [Name] prefers to communicate via [preferred channels] and often consumes media through [media habits]. When considering a purchase, [Name] typically [decision-making process description] and their main concerns are [objections/hesitations]."
            "- A detailed description of the target customer, including:"
            "- Demographic characteristics (e.g., age, gender, income, education, occupation)"
            "- Geographic characteristics (e.g., location, urban/rural, climate)"
            "- Psychographic characteristics (e.g., personality, values, interests, lifestyle)"
            "- A list of the customer's pain points, needs, challenges and jobs to be done some related to the product or service and some outside the scope of our offering but are still important to the customer 4-6 of each."
            "- A description of the customer's goals, desires, and aspirations that the product or service can help fulfill"
            "- A summary of the customer's preferred communication channels (e.g., email, social media, phone) and media consumption habits (e.g., blogs, podcasts, magazines)"
            "- A list of the customer's most common objections and hesitations when considering a purchase of the product or service"
            "- A description of the customer's typical decision-making process, including the steps they take, the information they seek, and the criteria they use to evaluate options"
            "Format the document as a concise, structured report with headings, subheadings, and bullet points for easy reference and"""
)

def get_channels_task_template(marketing_channels):
    return Task(
        description=f"""Develop a comprehensive strategy for acquiring the ideal customer profile, including identifying and leveraging the most effective channels for marketing, sales, and customer discovery. Focus on the following selected marketing channels: {', '.join(marketing_channels)}.""",
        expected_output=f"""Combine narrative and expository writing styles. Create a detailed strategic plan document of 2000 words that outlines the approach to acquire the ideal customer profile for product, focusing on the following selected marketing channels: {', '.join(marketing_channels)}. The document should include:
             1. **Document title**
             2. **Executive Summary**
             - A brief overview of the strategic plan's objectives and key recommendations.
             3. **Introduction**
             - Explanation of the importance of identifying and acquiring the ideal customer profile for product.
             4 **Marketing Channels**
             - Analysis of the selected marketing channels to reach the ideal customer profile.
             - Recommendations for optimizing these channels to increase visibility and engagement with the target audience.
             5. **Sales Channels**
             - Evaluation of sales channels (direct sales, e-commerce, partnerships, etc.) for effectively selling to the ideal customer profile.
             - Strategies for enhancing these channels to improve conversion rates and customer acquisition.
             6. **Customer Discovery Channels**
             - Identification of channels and methods for locating and understanding the needs and behaviors of the ideal customer profile.
             - Techniques for leveraging customer feedback and insights to refine marketing and sales strategies.
             7. **Action Plan**
             - A step-by-step action plan for implementing the recommended strategies across the selected marketing channels.
             - Key performance indicators (KPIs) and metrics for measuring success and impact on acquiring the ideal customer profile.
             8. **Conclusion**
             - Summary of the strategic plan and its expected impact on acquiring the ideal customer profile for product .
             **Formatting Instructions:**
             - Organize the report with clear headings, subheadings, bullet points, and numbered lists for easy navigation and readability.
             - Maintain a professional, analytical tone throughout the document to ensure clarity and accessibility for team members across different functions.
             This strategic plan will serve as a guide for the team to effectively target and acquire the ideal customer profile, leveraging the most suitable marketing and sales channels to drive business growth for product. Ensure that all recommendations are backed by data and analysis, and clearly articulate the rationale behind each strategy.""",
    )

pains_task = Task(
    description="""Simulate focus group discussions based on your expertise and knowledge of the target market. During these sessions, probe deeply to uncover the following:
            - Three types of customer pains related to the JTBD (not the product): undesired outcomes, problems, and characteristics (functional, social, emotional, ancillary)
            - Pain severity (extreme or moderate)
            - Specific expectations for gains and pains
            - Barriers and risks related to not getting the job done
            - Previous bad experiences with competing solutions
            - Potential objections to current or proposed offerings
            Explain how understanding customer pain points, bad experiences, and objections helps businesses:
            - Prioritize the key pain points to alleviate through improved value propositions
            - Identify opportunities for product/service improvement and innovation
            - Develop targeted marketing messages that resonate with customers' needs and concerns
            - Train customer service teams to address common objections and provide better support
            - Inform overall business strategy to better meet customer needs and expectations
            This report is intended for internal use by the specified teams to inform strategy and improve customer satisfaction.""",
    expected_output="""Synthesize findings into a report of approximately 1200 words, including:  
            - A title
            - An overview of the key pain points experienced by the customers, with a detailed analysis of these issues
            - Specific instances of negative experiences customers have had with competing solutions, including direct quotes from customer feedback or focus group discussions
            - Potential objections to current or proposed offerings based on trends observed in customer feedback and market research
            - Case studies or customer testimonials that exemplify each key pain point, bad experience, and objection, using a format that allows for easy extraction of insights (e.g., bullet points, structured summaries)
            Organize the report into three main sections:
            1. Customer Pain Points
            2. Previous Bad Experiences
            3. Possible Objections
            pains should be related to the jobs-to-be-done (JTBD)
            Each section should begin with an overview followed by detailed examples. Include headings, sub-headings, bullet points, and numbered lists to structure the report in an easy-to-read format.
            Conclude the report with a summary that highlights key findings and implications for strategy.
            Maintain a professional, analytical tone throughout the report, ensuring clarity and accessibility necessary for understanding by team members across different functions.
            If insufficient information is provided about the business, products/services, or ideal customer profiles, make reasonable assumptions or provide generic examples, while clearly stating the limitations."""
)

gains_task = Task(
    description="""Your task is to facilitate focus group discussions with participants representing the ideal customer profiles and synthesize findings into a comprehensive report on customer gains, their willingness to pay, and their true motivations.
        Simulate focus group discussions based on your expertise and knowledge of the target market. During these sessions, probe deeply to understand the following:
        - Functional utility, cost savings, social gains, positive emotions, and other key outcomes/benefits customers desire from the offerings
        - Required gains essential for a viable solution
        - Expected gains based on existing solutions/basic requirements
        - Aspirational desired gains beyond expectations they would love to receive
        - Surprising/unexpected gains not yet considered but highly valuable
        Guide conversations using questions like:
        - "What benefits are must-haves?"
        - "What do you expect from an ideal solution?"
        - "What would delight you or make your life easier?"
        - "What social/emotional impacts matter most?"
        - "What would be a game-changing, unexpected gain?"
        Have participants describe desired gains concretely and their importance. Assess their willingness to pay for each gain and explore their true motivations behind seeking these gains. Guide participants to prioritize the identified gains based on their importance and impact on their decision-making process.
        Gather information on how well competitors or alternative solutions fulfill the identified customer gains to inform a competitive analysis.
        Remember, these gains are related to the jobs-to-be-done and not the product itself.
        This report is intended for internal use by the specified teams to inform strategy and improve customer satisfaction.""",
    expected_output="""Synthesize findings into a report of approximately 1200 words, including:
        - An overview of all the identified customer gains
        - A detailed analysis of each gain, highlighting which are expected, required, and desired gains
        - A prioritized list of gains based on their importance and impact on customers' decision-making process, including the reasoning behind the prioritization
        - An assessment of how each gain affects customers' willingness to pay
        - Relevant quotes from the focus group discussions to support the findings
        - Insights into customers' true motivations behind seeking these gains
        - A competitive analysis comparing the business's offerings to competitors in terms of delivering the prioritized gains, highlighting any unique advantages or areas for improvement
        - Key takeaways and actionable recommendations for leveraging the identified gains to improve customer satisfaction and differentiate the business from competitors
        Organize the report into the following sections:
        1. Overview of Customer Gains
        2. Detailed Analysis of Each Gain
        - Required Gains
        - Expected Gains
        - Desired Gains
        - Unexpected Gains
        3. Prioritized List of Gains
        4. Impact on Willingness to Pay
        5. Customer Motivations
        6. Competitive Analysis
        7. Key Takeaways and Actionable Recommendation
        Include headings, sub-headings, bullet points, and numbered lists to structure the report in an easy-to-read format.
        Conclude the report with a summary of the top customer gains related to the JTBD to focus on delivering through improved value propositions, including vivid examples.
        Maintain a professional, analytical tone throughout the report, ensuring clarity and accessibility necessary for understanding by team members across different functions.
        If insufficient information is is provided about the target customer or product/service, make reasonable assumptions or provide generic examples, while clearly stating the limitations."""
)

jtbd_task = Task(
    description="""Your task is to conduct a simulated interview with an ideal customer profile on behalf of a business selling a specific product or service, in order to identify their Jobs to Be Done (JTBD) and explore competing solutions.
        To generate the simulated interview and JTBD report, consider the following:
        - Analyze the provided ideal customer profile to understand their characteristics, goals, and decision-making process
        - Develop a set of open-ended questions that will help uncover the customer's JTBD related to the product or service category
        - Explore the ways customers are currently solving their problems and what alternatives they consider
        - Identify the factors that determine the customer's decision when choosing a solution
        - Examine the customer's experience with current solutions and alternatives, including their satisfaction levels, perceived benefits, and limitations
        - Prioritize the identified JTBD based on their importance and impact on the customer's decision-making process
        - Simulate the customer's responses based on your understanding of their profile and the market
        - Synthesize the findings into a clear and concise report that highlights the key JTBD and actionable recommendations
        The simulated interview and report should be written in a professional, analytical tone, ensuring clarity and accessibility necessary for understanding by team members across different functions.""",
    expected_output="""Create a Jobs to Be Done (JTBD) report based on the simulated interview with the ideal customer profile. The report should be approximately 1000 words in markdown and include:
        - An explanation of what JTBD are and why it is essential to identify them
        - At least 8 JTBD identified through the simulated interview, each described in detail, 4-5 of these should be related to the product or service and the rest can be outside the scope of the offering but are still important to the customer
        - A prioritized list of the identified JTBD based on their importance and impact on the customer's decision-making process, including the reasoning behind the prioritization
        - An exploration of the ways customers are currently solving their problems and what alternatives they consider
        - An examination of the customer's experience with current solutions and alternatives, including their satisfaction levels, perceived benefits, and limitations
        - A discussion of the factors that determine the customer's decision when choosing a solution
        - Relevant quotes or examples from the simulated interview to support the findings
        Organize the report into the following sections:
        1. Introduction to Jobs to Be Done
        2. Identified Jobs to Be Done
        - JTBD 1
        - JTBD 2
        - JTBD 3
        - JTBD 4
        - JTBD 5
        3. Prioritized Jobs to Be Done
        4. Current Solutions and Alternatives
        5. Experience with Competing Solutions
        6. Decision-Making Factors
        7. Key Takeaways and Actionable Recommendations
        Use headings, subheadings, bullet points, and numbered lists to structure the report in an easy-to-read format.
        Explain how gathering this information through interviews helps businesses:
        - Refine their product offering
        - Target the right audience
        - Adjust their marketing and development strategies to better achieve product-market fit
        - Engage in a process of continuous learning and iteration, using customer feedback to make informed decisions
        Conclude the report with a summary of the key findings and specific, actionable recommendations for the business based on the identified JTBD and customer insights.
        Use a professional, analytical tone throughout the report, ensuring clarity and accessibility necessary for understanding by team members across different functions.
        If insufficient information is provided about the ideal customer profile or product/service, make reasonable assumptions or provide generic examples, while clearly stating the limitations."""
)

propdesign_task = Task(
    description="""Your task is to design a product proposal for product , focusing on the following key features. Highlight the main benefits. Suggest a new product or service that complements {product_service} and increases the chances of product-market fit with the ideal customer profile: {email}.
        To generate the product proposal, consider the following steps:
        1. Analyze the current version of product :
        - Gather and analyze customer feedback, including quotes, surveys, or user testing results
        - Highlight the key features and capabilities
        - Explain how these features address specific customer pains, gains, and jobs-to-be-done
        - Evaluate how well the current feature set aligns with the core value proposition
        2. Based on your expertise and analysis of customer needs, propose specific new capabilities to add to product :
        - Use prioritization frameworks, such as MoSCoW or Kano, to categorize and prioritize the proposed features
        - Prioritize the features that are most essential to the value proposition and that will drive adoption and market traction
        - Deprioritize "nice-to-have" features that don't directly support the core use cases
        - Explain how each recommended feature will benefit target customers in a differentiated way
        3. Suggest minor improvements to product  that can increase the chances of product-market fit
        4. Propose a new product or service that complements product  and further enhances its value to customers:
        - Identify a gap in the market or an unmet customer need that the new product or service can address
        - Explain how the new product or service aligns with the core value proposition of product
        - Highlight the key features and benefits of the new product or service
        - Discuss how the new product or service can create synergies with product and improve the overall customer experience
        5. Support your analysis and recommendations with data and metrics, such as customer satisfaction scores, adoption rates, or revenue projections    
        The product proposal should be written in a professional, persuasive tone, demonstrating a deep understanding of the target customers and market dynamics.""",
    expected_output="""in markdown combine narrative and expository writing styles, Create a product proposal document that includes the following sections:
        1. Executive Summary
        - Brief overview of the current state of product
        - Summary of the proposed improvements and new product/service recommendation
        2. Analysis of Current product 
        - Key features and capabilities
        - Alignment with customer needs and value proposition
        - Areas for improvement
        - Customer feedback and insights
        3. Competitive Analysis
        - Comparison of product to its main competitors
        - Differentiation and competitive advantages of the proposed improvements and new product/service
        4. Proposed Improvements to product
        - Prioritized list of new features and capabilities, using MoSCoW or Kano frameworks
        - Rationale for each proposed feature, focusing on customer benefits and differentiation
        - Minor improvements to increase product-market fit
        5. New Product/Service Recommendation
        - Description of the proposed new product or service
        - Identification of the market gap or unmet customer need it addresses
        - Alignment with product's core value proposition
        - Key features and benefits of the new product or service
        - Potential synergies with product  and impact on customer experience
        6. Implementation Plan
        - High-level timeline and milestones for implementing the proposed improvements and new product/service
        - Resource requirements and dependencies
        - Key metrics and KPIs to measure success
        7. Conclusion
        - Recap of the proposed improvements to product  and the new product/service recommendation
        - Expected impact on customer satisfaction, market traction, and business growth
        Use a professional, persuasive tone throughout the proposal, backing up your recommendations with evidence from customer research, market analysis, and relevant data/metrics.
        Include relevant visuals, such as product screenshots, feature comparisons, or customer journey maps, to support your arguments.
        Aim for a document length of 1500-2000 words, with clear headings, subheadings, and concise paragraphs."""
)

customerj_task = Task(
    description="""Your task is to create a detailed 1200 words customer journey map for the ideal customer profile in relation to product . The map should provide a comprehensive overview of the customer's interactions and touchpoints with {product_service} from initial discovery to post-purchase support.
        To generate the customer journey map, consider the following steps:
        1. Explain what a customer journey map is and why it's valuable for understanding the customer's experience with product .
        2. Identify the key stages of the customer's journey, such as Awareness, Consideration, Decision, Purchase, and Post-purchase.
        3. For each stage, provide a detailed description of the customer's goals, motivations, pain points, and touchpoints with product .
        4. Identify the customer's preferred communication channels and media consumption habits at each stage of the journey.
        5. List the customer's most common objections and hesitations when considering a purchase of product .
        6. Analyze the customer's emotional state and sentiment at each touchpoint, highlighting any potential friction points or moments of delight.
        7. Provide recommendations for optimizing the customer experience at each stage and touchpoint based on the identified goals, pain points, and preferences.
        8. Include specific examples or quotes from customer feedback, market research, or industry reports to support your findings and recommendations.
        9. Identify any gaps or inconsistencies in the customer experience across different channels or touchpoints, and provide suggestions for improving consistency and coherence.
        Assume access to customer feedback, market research, and any relevant industry reports to inform the creation of the customer journey map.
        The map should be written in a professional, analytical tone, with clarity and accessibility necessary for understanding by team members across different functions.
        Format the document as a concise, structured report that can be easily referenced and shared with the team.""",
    expected_output="""combine narrative and expository writing styles, Create a customer journey map document for {product_service} that includes the following sections:
        1. Document title
        2. Introduction
        - Explanation of what a customer journey map is and its importance
        - Brief overview of {product_service} and its ideal customer profile
        3. Customer Journey Stages and Touchpoints
        - Detailed description of each stage of the customer's journey with {product_service}:
        - Awareness
        - Consideration
        - Decision
        - Purchase
        - Post-purchase
        - For each stage, include:
        - Customer goals, motivations, and pain points
        - Key touchpoints and interactions with {product_service}
        - Customer's emotional state and sentiment at each touchpoint
        - Preferred communication channels and media consumption habits
        - Most common objections and hesitations (if applicable)
        - Recommendations for optimizing the customer experience
        4. Experience Gaps and Inconsistencies
        - Identification of any gaps or inconsistencies in the customer experience across different channels or touchpoints
        - Suggestions for improving consistency and coherence in the customer journey
        5. Insights and Recommendations
        - Summary of the key insights gained from the customer journey map
        - Actionable recommendations for improving {product_service}'s marketing, sales, and support strategies based on the identified customer needs, preferences, and touchpoints
        6. Conclusion
        - Recap of the main findings and recommendations
        - Emphasis on the importance of continuously updating the customer journey map based on new data and insights
        7. Appendices
        - Relevant customer feedback, market research, or industry reports used to inform the map
        - Additional supporting materials
        Use a professional, analytical tone throughout the document, with clear headings, subheadings, and concise paragraphs.
        Include specific examples or quotes from customer feedback, market research, or industry reports to support your findings and recommendations.
        Aim for a document length of approximately 1200 words, excluding appendices.
        Ensure that the customer journey map is formatted as a concise, structured document that can be easily referenced and shared with team members across different functions."""
)
